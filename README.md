# HTTA Legends – AI Challenge 2025

> "Chỉ sống một lần, hãy sống sao không hối tiếc!"  
> Hãy cùng **HTTA Legends** bước vào hành trình AI Challenge, nơi chúng tôi biến ý tưởng thành sản phẩm, dữ liệu thành trải nghiệm, và truy vấn thành kết quả tức thì.

---

## 🏆 Giới thiệu Team

**Tên team:** HTTA Legends  
**Trưởng nhóm:** Vỏ Văn Tài  
**Thành viên:**  
- Huỳnh Chí Phi Thuận (Thuận mắt lé)  
- Phan Nguyễn Vũ Huy  
- Nguyễn Hoàng Ân  

**Sứ mệnh:** Tạo ra một **hệ thống AI đa phương tiện thông minh**, có thể xử lý **truy vấn tiếng Việt** và tìm kiếm **ảnh, video, audio** theo ngữ nghĩa, nhanh chóng và chính xác.  

---

## 🎯 Mục tiêu Dự án

1. Xây dựng **MVP hoàn chỉnh** với 4 thành phần chính:  
   - **Giao diện người dùng:** Nhập văn bản/giọng nói, hiển thị kết quả multimedia.  
   - **Xử lý truy vấn (NLP/LLM):** Phân tích intent + entity, hỗ trợ tiếng Việt, sinh câu trả lời tự nhiên.  
   - **Trợ lý ảo & điều phối:** Gợi ý truy vấn, xử lý truy vấn chưa rõ ràng.  
   - **Tìm kiếm đa phương tiện:** Semantic search, xếp hạng kết quả ảnh/video/audio.  

2. **Dữ liệu mẫu:**  
   - Kho dữ liệu vài trăm ảnh/video/audio đã gắn nhãn.  
   - File metadata: `metadata.json` hoặc `index.pkl` hỗ trợ tìm kiếm.  

3. **Demo mượt mà & tài liệu:**  
   - Mã nguồn, báo cáo kỹ thuật, hướng dẫn sử dụng đầy đủ.  
   - Truy vấn thử trên máy giám khảo phải nhanh, chính xác.  

---

## 🔧 Kiến trúc hệ thống

### 1. Tiền xử lý dữ liệu Video
- Trích xuất **keyframes** từ video (OpenCV/PyTorch Video).  
- Chỉ lấy khung hình quan trọng → giảm tải xử lý.  
- Tạo **vector embedding** cho hình ảnh + văn bản (CLIP).  
- Lưu trữ embedding + metadata trong **Milvus Vector Database**.  

### 2. Xử lý truy vấn
- Chuyển truy vấn người dùng (văn bản hoặc hình ảnh) thành **vector nhúng**.  
- Tìm kiếm trong **Milvus** theo **cosine similarity**, trả về Top-K kết quả nhanh nhất.  

### 3. Xuất kết quả & giao diện
- Hiển thị **video + keyframe + metadata** chính xác.  
- Giao diện **Streamlit/Gradio** trực quan, hỗ trợ người dùng nhập truy vấn, xem kết quả, refine search.  

---

## ⚙️ Công nghệ sử dụng
- **Vector Database:** Milvus  
- **Model tìm kiếm ngữ nghĩa:** CLIP / BLIP-2  
- **Xử lý NLP/LLM:** HuggingFace Transformers, LangChain, VnCoreNLP  
- **Giao diện web demo:** Streamlit, Gradio  
- **Tool bổ trợ:** Docker, Python, FAISS  

---

## 👥 Phân công vai trò

| Thành viên | Vai trò chính | Nhiệm vụ chính | Công cụ/Mô hình |
|------------|---------------|----------------|----------------|
| Vỏ Văn Tài | Trưởng nhóm / Kiến trúc hệ thống | Thiết kế pipeline, tích hợp NLP+Vision, benchmark hệ thống, quản lý tiến độ | Python, Docker, REST API |
| Nguyễn Hoàng Ân | NLP/LLM | Xử lý truy vấn tiếng Việt, sinh câu trả lời, tích hợp LLM | HuggingFace, LangChain, GPT/LLaVA |
| Phan Nguyễn Vũ Huy | Vision AI | Tạo embedding, tìm kiếm ảnh/video/audio | OpenCV, PyTorch, CLIP, FAISS |
| Huỳnh Chí Phi Thuận | Frontend/UI | Giao diện demo web, hiển thị kết quả mượt | Streamlit, Gradio, ReactJS |

---

## 🚀 Tại sao chọn Milvus + CLIP?

- **CLIP:** hiểu mối quan hệ hình ảnh & văn bản cực tốt, không cần huấn luyện lại.  
- **Milvus:** Vector DB mạnh mẽ, xử lý nhanh các truy vấn semantic search, phù hợp MVP.  
- **RAG + Keyframes:** Kết hợp retrieval-augmented generation với keyframes giúp truy xuất dữ liệu chính xác mà vẫn tối ưu thời gian.  

---

## 🌟 Tinh thần HTTA Legends

> “Chỉ sống một lần, hãy sống sao không hối tiếc.”  
> Mỗi dòng code, mỗi model, mỗi vector embedding đều là dấu ấn của HTTA Legends trên hành trình AI Challenge 2025.  
> Không chỉ là thắng giải, mà là trải nghiệm, học hỏi, và để lại dấu ấn khó quên.  

---

## 🔗 Tham khảo & tài liệu

- [AI Challenge 2025 – Thông tin](https://codalab.lisn.upsaclay.fr/competitions/20122)  
- [VBS2024 Teams & Systems](https://videobrowsershowdown.org/teams/vbs2024-systems/)  
- [RAG Chatbot Guide](https://csc.edu.vn/tin-tuc/Blog-chia-se/kham-pha-rag-huong-dan-xay-dung-chatbot-voi-rag-8433)  
- [CLIP Model Documentation](https://huggingface.co/docs/transformers/model_doc/clip)  
- [Vector Search ChromaDB](https://realpython.com/chromadb-vector-database/)  
