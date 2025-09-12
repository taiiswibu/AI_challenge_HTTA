import streamlit as st
from pathlib import Path
from PIL import Image
import pandas as pd
from deep_translator import GoogleTranslator
from search import search_videos_by_text, format_search_results_multi
from helpers import keyframe_path_from_frame_idx_multi_auto

# ===================== CONFIG =====================
st.set_page_config(
    layout="wide", 
    page_title="Hệ thống truy vấn thông minh",
    page_icon="🎯"
)
st.title("🎯 Hệ thống truy vấn thông minh")
st.markdown("""
<style>
.stApp { background-color: #f9fafc; font-family: 'Segoe UI', sans-serif; }
.stContainer { border: 1px solid #007BFF; border-radius: 10px; padding: 12px; margin-bottom: 20px; background-color: #ffffff; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
.video-title { font-size: 18px; font-weight: bold; color: #007BFF; }
.frame-info { font-size: 13px; background: #f1f5f9; padding: 6px; border-radius: 6px; margin-bottom: 8px; }
.section-header { font-size: 16px; font-weight: bold; margin-top: 10px; margin-bottom: 5px; }
</style>
""", unsafe_allow_html=True)

# ===================== INPUT =====================
query_vi = st.text_input("📝 Nhập nội dung muốn tìm:")

with st.expander("⚙️ Tùy chọn nâng cao"):
    top_k = st.slider("Số kết quả muốn hiển thị (top_k)", min_value=5, max_value=50, value=20, step=5)
    search_mode = st.selectbox("Chế độ tìm kiếm", options=["fast", "balanced", "accurate"], index=1, help="fast: nhanh nhưng ít chính xác, balanced: cân bằng, accurate: chính xác nhất nhưng chậm hơn")
    batch_select = st.multiselect("Chọn batch dữ liệu", options=["Batch1", "Batch2"], default=["Batch1", "Batch2"])

# ===================== XỬ LÝ =====================
if query_vi:
    with st.spinner("⏳ Đang tìm kiếm..."):
        try:
            # Dịch sang tiếng Anh
            query_en = GoogleTranslator(source='vi', target='en').translate(query_vi)

            # Lọc batch
            from config import CSV_DIRS, FRAME_DIRS
            selected_csv_dirs = []
            selected_frame_dirs = []
            if "Batch1" in batch_select:
                selected_csv_dirs.append(CSV_DIRS[0])
                selected_frame_dirs.append(FRAME_DIRS[0])
            if "Batch2" in batch_select:
                selected_csv_dirs.append(CSV_DIRS[1])
                selected_frame_dirs.append(FRAME_DIRS[1])

            # Thực hiện tìm kiếm
            search_results = search_videos_by_text(query_en, top_k=top_k, mode=search_mode)
            results = format_search_results_multi(search_results)

            st.markdown(f"### ✅ Kết quả cho: \"{query_vi}\"")
            st.caption(f"(Dịch sang Tiếng Anh: \"{query_en}\")")

            if not results: 
                st.info("❌ Không tìm thấy kết quả nào. Thử từ khóa khác.")
            else:
                # ===== Thống kê kết quả =====
                summary_data = []
                for video_path, (video_name, frames) in results.items():
                    frame_idxs = [f[0] for f in frames]
                    summary_data.append({
                        "Tên video": video_name,
                        "Đường dẫn": video_path,
                        "Frame Idx": frame_idxs,
                        "Số lượng frame": len(frames)
                    })
                st.dataframe(pd.DataFrame(summary_data), use_container_width=True)

                # ===== Hiển thị video + frame =====
                main_cols = st.columns(3)
                col_idx = 0
                for video_path, (video_name, frames) in results.items():
                    with main_cols[col_idx % 3]:
                        st.markdown(f"<div class='video-title'>🎬 {video_name}</div>", unsafe_allow_html=True)
                        st.caption(f"📂 `{video_path}`")
                        if Path(video_path).exists():
                            st.video(str(video_path))
                        else:
                            st.warning("⚠️ Video không tồn tại!")

                        if frames:
                            st.markdown("<div class='section-header'>🖼️ Frame Idx:</div>", unsafe_allow_html=True)
                            sub_cols = st.columns(2)
                            for i, (frame_idx, time_start, time_end, img_path) in enumerate(frames[:4]):
                                with sub_cols[i % 2]:
                                    if not img_path or not Path(img_path).exists():
                                        img_path = keyframe_path_from_frame_idx_multi_auto(video_path, frame_idx)
                                    if img_path and Path(img_path).exists():
                                        st.image(Image.open(img_path), use_column_width=True)
                                        st.markdown(f"""
                                            <div class="frame-info">
                                            <b>🖼 Frame Idx:</b> {frame_idx}<br>
                                            <b>⏱ Xuất hiện:</b> {time_start} → {time_end}<br>
                                            <b>📍 Path:</b> {img_path}
                                            </div>
                                        """, unsafe_allow_html=True)
                                    else:
                                        st.error(f"⚠️ Không tìm thấy ảnh cho frame {frame_idx}")
                    col_idx += 1
        except Exception as e:
            st.error(f"🚨 Lỗi trong quá trình tìm kiếm: {e}")
