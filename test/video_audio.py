from faster_whisper import WhisperModel

model_size = "large-v3-turbo"

model = WhisperModel(model_size, device="cpu", compute_type="int8")
segments, info = model.transcribe("data.wav", beam_size=5, language="vi", condition_on_previous_text=False, vad_filter=True)

for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))