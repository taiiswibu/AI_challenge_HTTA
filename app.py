# app.py
import streamlit as st
import os
from deep_translator import GoogleTranslator
from your_module import search_videos_by_text, format_search_results, CSV_DIR  # import các hàm bạn đã viết

st.set_page_config(page_title="Video Search", layout="wide")
st.title("🔍 Video Search with Frame Preview")

# ---------------- Input Query ----------------
query_text = st.text_input("Nhập truy vấn (tiếng Việt):", "")

top_k = st.slider("Số lượng kết quả tối đa:", 1, 50, 20)
gap_threshold = st.slider("Khoảng cách nhóm timestamps (giây):", 5, 60, 15)

if query_text:
    # Dịch sang tiếng Anh
    query_en = GoogleTranslator(source='vi', target='en').translate(query_text)

    st.markdown(f"**Query dịch sang tiếng Anh:** {query_en}")

    # Tìm kiếm video
    search_results = search_videos_by_text(query_en, top_k=top_k, gap_threshold=gap_threshold)

    # Chuyển thành format có frame_idx + ảnh
    results = format_search_results(search_results, csv_dir=CSV_DIR)

    # Hiển thị kết quả
    for video_path, (video_name, frames) in results.items():
        st.subheader(f"🎬 {video_name}")
        st.write(f"Path: {video_path}")

        for frame_idx, time_start, time_end in frames:
            # Tạo đường dẫn ảnh dựa trên frame_idx
            video_base = os.path.splitext(os.path.basename(video_path))[0]
            img_path = os.path.join("/home/shared/data_batch1/Keyframes", video_base, f"{frame_idx}.jpg")
            if os.path.exists(img_path):
                st.markdown(f"**Frame Idx:** {frame_idx} -- Xuất hiện từ {time_start} đến {time_end}")
                st.image(img_path, width=320)  # hiển thị ảnh trực tiếp
            else:
                st.markdown(f"**Frame Idx:** {frame_idx} -- Xuất hiện từ {time_start} đến {time_end} -- Ảnh không tồn tại")


# (milvus_env) thuan@instance-20250820-145528:/home/shared/CODE_cua_Thuan$ export PATH=$PATH:/home/thuan/.local/bin
# (milvus_env) thuan@instance-20250820-145528:/home/shared/CODE_cua_Thuan$ streamlit run app.py