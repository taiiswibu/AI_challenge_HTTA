import os
import subprocess
from faster_whisper import WhisperModel

VIDEO_PATH = "../../../Data/AIC2025/Videos"
DATA_PATH = "../../data"
TRANSCRIPT_PATH = "../../data/transcript"
AUDIO_PATH = "../../data/audio"

model_size = "large-v3-turbo"
model = WhisperModel(model_size, device="cpu", compute_type="int8")


def video_to_audio(base_input_path, base_output_path):
    assert os.path.exists(base_input_path) and os.path.exists(base_output_path), \
        "Đường dẫn không tồn tại"

    for video_part in os.listdir(base_input_path):
        video_part_path = os.path.join(base_input_path, video_part, "video")

        if not os.path.isdir(video_part_path):
            continue

        for video in os.listdir(video_part_path):
            video_path = os.path.join(video_part_path, video)
            video_name = os.path.splitext(os.path.basename(video_path))[0]

            output_part_path = os.path.join(base_output_path, video_part)
            os.makedirs(output_part_path, exist_ok=True)

            output_file = os.path.join(output_part_path, f"{video_name}.wav")

            if os.path.exists(output_file):
                continue

            print("Convert:", video_path)

            try:
                subprocess.run(
                    [
                        "ffmpeg", "-y",         # -y để ghi đè file nếu có
                        "-i", video_path,
                        "-vn",
                        "-acodec", "pcm_s16le",
                        "-ar", "44100",
                        "-ac", "2",
                        output_file
                    ],
                    check=True,
                    stdout=subprocess.DEVNULL,  # ẩn log nếu không cần
                    stderr=subprocess.STDOUT
                )
            except subprocess.CalledProcessError as e:
                print(f"❌ Lỗi khi convert {video_path}: {e}")
                continue  # sang file tiếp theo


def audio_to_transcript(base_input_path, base_output_path):
    assert  os.path.exists(base_input_path) or \
            os.path.exists(base_output_path), \
            "Đường dẫn không tồn tại"
    
    # Load model
    model_size = "large-v3-turbo"
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    
    # Duyệt từng phần
    for audio_part in os.listdir(base_input_path):
        audio_part_path = os.path.join(base_input_path, audio_part)

        # Tạo output part nếu chưa tồn tại
        output_part_path = os.path.join(base_output_path, audio_part)
        if not os.path.exists(output_part_path):
            os.mkdir(output_part_path)

        # Duyệt từng audio
        for audio in os.listdir(audio_part_path):
            audio_path = os.path.join(audio_part_path, audio)
            audio_name = os.path.splitext(os.path.basename(audio_path))[0]

            print(f"Tiến hành đọc văn bản {audio_name}")
            segments, _ = model.transcribe(f"{audio_path}", beam_size=5, language="vi", condition_on_previous_text=False, vad_filter=True)

            with open(f"{output_part_path}/{audio_name}.txt", "w", encoding="utf-8") as f:
                for segment in segments:
                    f.write(f"{segment.text}\n")


if __name__ == "__main__":
    pass