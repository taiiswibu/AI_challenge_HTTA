import torch

# ================= DB & Milvus =================
DB_PARAMS = {
    "dbname": "video_db",
    "user": "postgres",
    "password": "123",
    "host": "localhost",
    "port": "5432"
}

CSV_DIRS   = ["/home/shared/data_batch1/map-keyframes/", "/home/shared/batch2/map-keyframes/"]
FRAME_DIRS = ["/home/shared/data_batch1/Keyframes/", "/home/shared/batch2/Keyframes/"]

MODEL_DIR  = "/home/shared/huggingface_cache"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
