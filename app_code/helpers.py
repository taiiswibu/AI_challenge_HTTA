import os, glob, pandas as pd, torch, torch.nn.functional as F
from functools import lru_cache
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from .config import device, MODEL_DIR, CSV_DIRS, FRAME_DIRS

# ================= CLIP =================
clip_model = CLIPModel.from_pretrained(
    "openai/clip-vit-base-patch32",
    cache_dir=MODEL_DIR
).to(device)
clip_processor = CLIPProcessor.from_pretrained(
    "openai/clip-vit-base-patch32",
    cache_dir=MODEL_DIR
)

# ================= Encode =================
def encode_text(text):
    try:
        inputs = clip_processor(
            text=[text],
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=77
        ).to(device)
        with torch.no_grad():
            text_features = clip_model.get_text_features(**inputs)
        return F.normalize(text_features, p=2, dim=1)[0].cpu().numpy()
    except Exception as e:
        print(f"Lỗi encode text: {e}")
        return None

def encode_image(image_path):
    try:
        image = Image.open(image_path)
        inputs = clip_processor(images=image, return_tensors="pt").to(device)
        with torch.no_grad():
            features = clip_model.get_image_features(**inputs)
        return features[0].cpu().numpy()
    except Exception as e:
        print(f"Lỗi encode image {image_path}: {e}")
        return None

# ================= Time & Frame =================
def time_to_seconds(time_str):
    try:
        m, s = map(int, time_str.split(':'))
        return m*60 + s
    except:
        try:
            return float(time_str)
        except:
            return None

def format_time(seconds):
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m}:{s:02d}"

def group_timestamps(frame_list, gap_threshold=15.0, margin=5.0, min_range=5.0):
    if not frame_list: return []
    frame_list = sorted(frame_list, key=lambda x: x[1])
    groups, current_group = [], [frame_list[0]]
    for i in range(1, len(frame_list)):
        _, prev_time = frame_list[i-1]
        f, cur_time  = frame_list[i]
        if cur_time - prev_time <= gap_threshold:
            current_group.append((f, cur_time))
        else:
            groups.append(current_group)
            current_group = [(f, cur_time)]
    groups.append(current_group)

    result = []
    for group in groups:
        start_time = max(0, group[0][1] - margin)
        end_time   = group[-1][1] + margin
        if end_time - start_time < min_range:
            end_time = start_time + min_range
        frame_idxs = [f for f, _ in group]
        result.append((start_time, end_time, frame_idxs))
    return result

# ====== CSV Cache ======
@lru_cache(maxsize=256)
def load_csv(video_name, csv_dir):
    path = os.path.join(csv_dir, f"{video_name}.csv")
    if not os.path.exists(path): return None
    df = pd.read_csv(path)
    if not all(c in df.columns for c in ["n", "frame_idx", "pts_time"]): return None
    return df

# ====== Keyframe Path ======
def keyframe_path_from_frame_idx_auto(video_path, frame_idx, csv_dir, frame_root):
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    df = load_csv(video_name, csv_dir)
    if df is None: return None

    idx = (df["frame_idx"] - int(frame_idx)).abs().idxmin()
    n_val = int(df.loc[idx, "n"])
    candidates_stem = [n_val, f"{n_val:03d}", f"{n_val:04d}", frame_idx, f"{int(frame_idx):03d}", f"{int(frame_idx):04d}"]

    possible_dirs = glob.glob(os.path.join(frame_root, "**", video_name), recursive=True)
    for dir_path in possible_dirs:
        for stem in candidates_stem:
            for ext in ("jpg","jpeg","png"):
                p = os.path.join(dir_path, f"{stem}.{ext}")
                if os.path.exists(p):
                    return p
    return None

def keyframe_path_from_frame_idx_multi_auto(video_path, frame_idx):
    for csv_dir, frame_root in zip(CSV_DIRS, FRAME_DIRS):
        path = keyframe_path_from_frame_idx_auto(video_path, frame_idx, csv_dir, frame_root)
        if path: return path
    return None

# ====== Frame từ time (multi-batch) ======
def get_frame_idx_from_time_multi(video_path, time_start, time_end):
    for csv_dir in CSV_DIRS:
        df = load_csv(os.path.splitext(os.path.basename(video_path))[0], csv_dir)
        if df is None: 
            continue
        start_sec = time_to_seconds(time_start)
        end_sec   = time_to_seconds(time_end)
        if start_sec is None or end_sec is None: 
            continue
        target_time = (start_sec + end_sec)/2
        idx = (df['pts_time'] - target_time).abs().idxmin()
        return int(df.loc[idx,'frame_idx']), csv_dir
    return None, None
