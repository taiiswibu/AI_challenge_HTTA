import os
import torch
from PIL import Image
from tqdm import tqdm
from transformers import AutoProcessor, Qwen2VLForConditionalGeneration

device = "cuda" if torch.cuda.is_available() else "cpu"
model_id = "Qwen/Qwen2-VL-2B-Instruct"

KEYFRAME_PATH = "../../../Data/AIC2025/Keyframes"
DESCRIBE_PATH = "../../data/describe"

# Load model + processor
model = Qwen2VLForConditionalGeneration.from_pretrained(
    model_id,
    torch_dtype=torch.float16,        # mixed precision
    low_cpu_mem_usage=True,
    device_map="auto"                 # tự động dàn trên GPU
)
processor = AutoProcessor.from_pretrained(model_id)


def describe_keyframe(base_input_path, base_output_path, batch_size=4):
    """
    Dùng mô hình để mô tả các keyframe và lưu về text
    """
    for part in os.listdir(base_input_path):
        part_path = os.path.join(base_input_path, part)
        if not os.path.isdir(part_path):
            continue

        keyframe_root = os.path.join(part_path, "keyframes")
        if not os.path.exists(keyframe_root):
            continue

        for video in os.listdir(keyframe_root):
            video_path = os.path.join(keyframe_root, video)
            if not os.path.isdir(video_path):
                continue

            # Tạo output folder
            output_video = os.path.join(base_output_path, part, video)
            os.makedirs(output_video, exist_ok=True)

            keyframes = [os.path.join(video_path, kf) for kf in os.listdir(video_path)]
            keyframes.sort()

            # Chia batch để chạy song song
            for i in tqdm(range(0, len(keyframes), batch_size), desc=f"Đang mô tả {video}"):
                batch_paths = keyframes[i:i+batch_size]
                batch_images = [Image.open(p).convert("RGB") for p in batch_paths]

                # Tạo prompt cho từng ảnh
                messages = [
                    {
                        "role": "user",
                        "content": [
                            {"type": "image", "image": img},
                            {"type": "text", "text": "Mô tả bức ảnh này bằng tiếng Việt thật chi tiết, súc tích."}
                        ]
                    }
                    for img in batch_images
                ]
                chat_template = [processor.apply_chat_template([m], add_generation_prompt=True) for m in messages]

                # Encode batch
                inputs = processor(
                    text=chat_template,
                    images=batch_images,
                    return_tensors="pt",
                    padding=True
                ).to(device)

                # Sinh mô tả với autocast để tăng tốc
                with torch.cuda.amp.autocast():
                    generated = model.generate(**inputs, max_new_tokens=128)

                outputs = processor.batch_decode(generated, skip_special_tokens=True)

                # Ghi file
                for p, out in zip(batch_paths, outputs):
                    keyframe_name = os.path.basename(p)
                    output_txt = os.path.join(output_video, f"{keyframe_name}.txt")
                    with open(output_txt, "w", encoding="utf-8") as f:
                        f.write(out)

describe_keyframe(KEYFRAME_PATH, DESCRIBE_PATH)