````{"id":"83925","variant":"standard","title":"README.md – ViviSearch (HTTA Legends AI Challenge 2025)"}
# 🎯 ViviSearch – Vietnamese Semantic Multimedia Search System  
### 🏆 HTTA Legends – AI Challenge 2025

> “Chỉ sống một lần, hãy sống sao không hối tiếc.”  

---

## 👥 Giới thiệu Team

**Tên đội:** HTTA Legends  
**Cuộc thi:** [AI Challenge 2025 – Thành phố Hồ Chí Minh](https://aichallenge.hochiminhcity.gov.vn/)  
**Trưởng nhóm:** Võ Văn Tài  
**Thành viên:**  
- Huỳnh Chí Phi Thuận  
- Phan Nguyễn Vũ Huy  
- Nguyễn Hoàng Ân  

**Nhiệm vụ:**  
Phát triển **hệ thống tìm kiếm đa phương tiện ngữ nghĩa tiếng Việt** (Semantic Multimedia Search System), cho phép người dùng **tìm ảnh, video, audio** bằng **ngôn ngữ tự nhiên** (text/voice).  
Hệ thống được tối ưu cho **CLIP + Milvus**, triển khai thực tế trên **Google Cloud (Ubuntu Linux)**.

---

## 🎯 Mục tiêu dự án

1. **Phát triển MVP hoàn chỉnh** gồm 3 module:  
   - 🧠 *Trợ lý ảo điều phối*: hiểu truy vấn tiếng Việt, gợi ý thêm ngữ cảnh.  
   - 🔍 *Tìm kiếm đa phương tiện*: CLIP + Milvus cho semantic search.  
   - 💻 *Giao diện người dùng*: nhập truy vấn text/voice, hiển thị kết quả multimedia.  

2. **Dữ liệu demo:**  
   - Kho ảnh, video, audio có nhãn ngữ nghĩa.  
   - Metadata quản lý bằng `metadata.json` hoặc `index.pkl`.

3. **Demo hoàn chỉnh:**  
   - Giao diện Streamlit trực quan, phản hồi nhanh.  
   - Báo cáo kỹ thuật và hướng dẫn triển khai trên Cloud.

---

## 🧩 Kiến trúc hệ thống

### ⚙️ Quy trình tổng quan
```
User Query → Text/Voice → Translate API → CLIP Encoder → Milvus Search → Retrieve Results → Streamlit UI
```

### 🔄 Quy trình chính
1. **Xử lý dữ liệu video:**  
   - Tách *keyframes* bằng OpenCV.  
   - Sinh embedding (CLIP/BLIP-2) cho ảnh/video/audio.  
   - Lưu vector vào **Milvus**, metadata vào **PostgreSQL**.  

2. **Xử lý truy vấn:**  
   - Người dùng nhập text hoặc ảnh → CLIP encoder → vector embedding.  
   - Milvus tìm Top-K kết quả gần nhất (cosine similarity).  

3. **Hiển thị kết quả:**  
   - Streamlit hiển thị multimedia + metadata.  
   - Cho phép lọc lại kết quả (theo tag, loại media, độ tương đồng).  

---

## 🧠 Công nghệ chính

| Thành phần | Công cụ / Framework | Mô tả |
|-------------|--------------------|-------|
| **Vector DB** | Milvus v2.4.1 | Lưu trữ & truy vấn embedding |
| **Embedding Model** | CLIP / BLIP-2 | Sinh vector text + ảnh |
| **Ngôn ngữ & NLP** | Google Translate API, VnCoreNLP | Chuẩn hóa & dịch truy vấn |
| **Frontend / Backend** | Streamlit, FastAPI | Giao diện và API chính |
| **Database** | PostgreSQL 15 | Lưu metadata |
| **Containerization** | Docker + Docker Compose | Đóng gói môi trường |
| **Cloud Hosting** | Google Cloud (GCP) | VM Ubuntu 25.04 (SSD + HDD) |

---

## ☁️ Hạ tầng Cloud (GCP)

**Nền tảng:** Google Cloud Compute Engine  

**Cấu hình VM:**
- 8 vCPU Intel® Xeon®  
- 32GB RAM  
- 250GB SSD (chạy hệ thống)  
- 280GB HDD (lưu dữ liệu media + embedding)  
- OS: Ubuntu 25.04 (Kernel 6.14.0-gcp)

> Tất cả thành viên được phân quyền SSH riêng, thao tác qua Linux CLI và Docker.

---

## ⚙️ Thiết lập môi trường

```bash
# Cập nhật & cài đặt cơ bản
sudo apt update && sudo apt upgrade -y
sudo apt install docker.io docker-compose python3-venv git -y
```

### 👤 Phân quyền người dùng Linux

```bash
# Tạo user riêng cho từng thành viên
sudo adduser thuan
sudo adduser huy
sudo adduser an

# Phân quyền thư mục project + data
sudo mkdir -p /home/ubuntu/AI_CHALLENGE_HTTA/data/{batch1,batch2}
sudo chown -R tai:htta /home/ubuntu/AI_CHALLENGE_HTTA

# Thêm quyền Docker
sudo usermod -aG docker thuan
sudo usermod -aG docker huy
sudo usermod -aG docker an
```

---

## 📂 Cấu trúc thư mục

```
AI_CHALLENGE_HTTA/
│
├── app_code/
│   ├── __init__.py
│   ├── config.py              # Đọc ENV (Postgres, Milvus, GCP)
│   ├── helpers.py             # Hàm tiện ích chung
│   ├── load_data.ipynb        # Chuẩn bị dữ liệu embedding
│   ├── search.py              # Logic tìm kiếm vector
│   └── create_postgres.ipynb  # Tạo bảng & import metadata
│
├── app.py                     # Main Streamlit app
├── docker-compose.yml         # Milvus + PostgreSQL container
├── requirements.txt           # Thư viện Python
├── README.md                  # Mô tả dự án
├── note_to_run_app.txt        # Ghi chú kỹ thuật
├── venv/                      # Virtual environment
└── data/                      # Lưu embedding & media
```

---

## 🚀 Hướng dẫn chạy hệ thống

```bash
# 1. Clone repo
git clone https://github.com/HTTA-Legends/AI_CHALLENGE_HTTA.git
cd AI_CHALLENGE_HTTA

# 2. Tạo môi trường ảo
python3 -m venv venv
source venv/bin/activate

# 3. Cài thư viện
pip install -r requirements.txt

# 4. Khởi chạy Docker services
docker-compose up -d

# 5. Chạy giao diện web
streamlit run app.py
```

> 💡 Ảnh & video demo sẽ được thêm sau khi hệ thống hoàn thiện.

---

## 👨‍💻 Phân công & Vai trò

| Thành viên | Vai trò | Nhiệm vụ | Kỹ năng chính |
|-------------|----------|-----------|----------------|
| **Võ Văn Tài** | Leader / Data Engineer | Thiết lập GCP, tối ưu pipeline, tích hợp CLIP + Milvus, build UI | Docker, Python, Streamlit, Milvus |
| **Nguyễn Hoàng Ân** | NLP Engineer | Xử lý tiếng Việt, dịch và chuẩn hóa truy vấn | HuggingFace, VnCoreNLP |
| **Phan Nguyễn Vũ Huy** | Vision Engineer | Tìm kiếm ảnh/video/audio, tối ưu CLIP embedding | PyTorch, OpenCV |
| **Huỳnh Chí Phi Thuận** | Backend Engineer | Xây dựng metadata DB, quản lý upload vector | PostgreSQL, Docker |

---

## 🌟 Điểm nổi bật

- **CLIP + Milvus:** Semantic Search ảnh/video/audio chính xác.  
- **Triển khai thật trên Google Cloud Linux.**  
- **Hệ thống Docker hóa:** dễ mở rộng và tái tạo môi trường.  
- **Tích hợp xử lý tiếng Việt + dịch tự động.**  

---

## 🧩 Kỹ năng nhóm học được

| Nhóm kỹ năng | Mô tả chi tiết |
|---------------|----------------|
| **AI/ML Systems** | CLIP, BLIP-2, Semantic Search, RAG pipeline |
| **Data Engineering** | Metadata schema, PostgreSQL integration |
| **DevOps & Cloud** | GCP setup, Docker Compose, Linux permissions |
| **Web & Visualization** | Streamlit UI, API integration, multimedia search |
| **Collaboration** | GitHub workflow, SSH multi-user, teamwork hiệu quả |

---

## 📚 Tài liệu tham khảo

- [AI Challenge 2025 – Website chính thức](https://aichallenge.hochiminhcity.gov.vn/)  
- [Video Browser Showdown 2024 Systems](https://videobrowsershowdown.org/teams/vbs2024-systems/)  
- [CLIP Model – HuggingFace](https://huggingface.co/docs/transformers/model_doc/clip)  
- [RAG Architecture – CSC Vietnam](https://csc.edu.vn/tin-tuc/Blog-chia-se/kham-pha-rag-huong-dan-xay-dung-chatbot-voi-rag-8433)  
- [Vector DB Comparison – RealPython](https://realpython.com/chromadb-vector-database/)  
- Radford, A. *et al.* (2021). *Learning Transferable Visual Models From Natural Language Supervision (CLIP)*.  
- Li, J. *et al.* (2023). *BLIP-2: Bootstrapping Language-Image Pre-training*.  
- Milvus Team. (2022). *Vector Database for AI Applications.*  
- Nguyen, H. *et al.* (2020). *VnCoreNLP: A Vietnamese NLP Toolkit.*

---

## 🎬 Demo & Liên hệ

📺 **Video demo:** [YouTube link (upcoming)](https://youtu.be/your_demo_link)  
📧 **Liên hệ:** Võ Văn Tài – *Data Engineer / AI Developer*  
✉️ Email: **vovantai2k4@gmail.com**  

---

> 🌠 Nếu bạn thấy dự án này thú vị, hãy **Star** repo để ủng hộ team **HTTA Legends**!
````
