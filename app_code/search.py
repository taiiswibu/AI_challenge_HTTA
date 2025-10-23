import os
import psycopg2
from pymilvus import connections, Collection
from .helpers import encode_text, group_timestamps, format_time, get_frame_idx_from_time_multi, keyframe_path_from_frame_idx_multi_auto
from .config import DB_PARAMS
from .helpers import get_frame_idx_from_time_multi, keyframe_path_from_frame_idx_multi_auto

# ================= Kết nối Database =================
conn = psycopg2.connect(**DB_PARAMS)
cur = conn.cursor()

# ================= Kết nối Milvus =================
# Nếu app chạy trên server host (venv) -> dùng localhost
# Nếu app chạy trong container khác -> đổi host="milvus-standalone"
connections.connect(
    alias="default",
    host="127.0.0.1",   # hoặc "milvus-standalone" nếu chạy Docker khác
    port="19530"
)

# Load collection 1 lần, tái sử dụng
collection = Collection("text_image_video_collection")
collection.load()
print("✅ Đã kết nối Milvus & load collection:", collection.name)


def search_videos_by_text(text_query, top_k=10, gap_threshold=15.0, margin=5.0, min_range=5.0, mode="balanced"):
    text_emb = encode_text(text_query)
    if text_emb is None: 
        return []

    ef_map = {"fast": 16, "balanced": 64, "accurate": 128}
    ef = ef_map.get(mode, 64)
    milvus_topk = top_k*3 if mode == "balanced" else top_k*5 if mode == "accurate" else top_k

    hits = collection.search(
        data=[text_emb.tolist()],
        anns_field="vector",
        param={"metric_type": "COSINE", "params": {"ef": ef}},
        limit=milvus_topk,
        output_fields=["id"]
    )[0]
    ids = [hit.id for hit in hits]
    if not ids: 
        return []

    # Lấy metadata từ Postgres
    cur.execute("""
        SELECT v.video_path, v.title, fm.frame_idx, fm.pts_time
        FROM frame_mappings fm
        JOIN videos v ON fm.video_id = v.id
        WHERE fm.milvus_id = ANY(%s)
    """, (ids,))
    rows = cur.fetchall()

    grouped_results = {}
    for video_path, title, frame_idx, pts_time in rows:
        if video_path not in grouped_results:
            grouped_results[video_path] = {"title": title, "frames": []}
        grouped_results[video_path]["frames"].append((frame_idx, pts_time))

    final_results = []
    for video_path, data in grouped_results.items():
        segments = group_timestamps(data["frames"], gap_threshold, margin, min_range)
        time_ranges = [(format_time(s), format_time(e)) for s, e, _ in segments]
        final_results.append({
            "video_path": video_path,
            "title": data["title"],
            "time_ranges": time_ranges
        })
    return final_results


def format_search_results_multi(search_results):
    grouped_results = {}
    for res in search_results:
        video_path = res['video_path']
        video_name = os.path.splitext(video_path)[0]
        grouped_results.setdefault(video_path, (video_name, []))
        for start_time, end_time in res['time_ranges']:
            frame_idx, _ = get_frame_idx_from_time_multi(video_path, start_time, end_time)
            if frame_idx is not None:
                img_path = keyframe_path_from_frame_idx_multi_auto(video_path, frame_idx)
                grouped_results[video_path][1].append((frame_idx, start_time, end_time, img_path))
    return grouped_results
