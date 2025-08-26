import torch
from transformers import AutoProcessor, Qwen2VLForConditionalGeneration
from PIL import Image

# Thiết bị
device = "cpu"
model_id = "Qwen/Qwen2-VL-2B-Instruct"

# Load model trên CPU
model = Qwen2VLForConditionalGeneration.from_pretrained(
    model_id,
    torch_dtype=torch.float32,
    low_cpu_mem_usage=True
).to(device)

processor = AutoProcessor.from_pretrained(model_id)

# Đọc ảnh từ đường dẫn
image_path = "test/sakura.jpg"
try:
    image = Image.open(image_path).convert("RGB")  # Chuyển ảnh sang định dạng RGB
except FileNotFoundError:
    raise FileNotFoundError(f"Không tìm thấy file ảnh tại: {image_path}")

# Prompt
messages = [
    {
        "role": "user",
        "content": [
            {"type": "image", "image": image},  # Truyền đối tượng PIL.Image
            {"type": "text", "text": "Mô tả bức ảnh này bằng tiếng Việt thật chi tiết, súc tích."}
        ]
    }
]

# Tạo input bằng cách sử dụng apply_chat_template
chat_template = processor.apply_chat_template(messages, add_generation_prompt=True)
inputs = processor(
    text=chat_template,  # Truyền template đã xử lý
    images=[image],  # Truyền danh sách ảnh
    return_tensors="pt"
).to(device)

# Sinh mô tả
generated = model.generate(**inputs, max_new_tokens=128)
output = processor.batch_decode(generated, skip_special_tokens=True)[0]
print("👉 Mô tả ảnh:", output)