
````{"id":"57302","variant":"standard","title":"README.md - HTTA Legends AI Challenge 2025 (final version)"}
# ViviSearch – Vietnamese Semantic Multimedia Search System
#  HTTA Legends – AI Challenge 2025

> “Chỉ sống một lần, hãy sống sao không hối tiếc.”  

---

##  Giới thiệu Team

**Tên đội:** HTTA Legends  
**Cuộc thi:** [AI Challenge 2025 – Thành phố Hồ Chí Minh](https://aichallenge.hochiminhcity.gov.vn/)  
**Trưởng nhóm:** Vỏ Văn Tài
**Thành viên:**  
- Huỳnh Chí Phi Thuận  
- Phan Nguyễn Vũ Huy  
- Nguyễn Hoàng Ân  

**Nhiệm vụ :**  
Xây dựng hệ thống tìm kiếm đa phương tiện ngữ nghĩa tiếng Việt (Semantic Multimedia Search System), có khả năng hiểu truy vấn tự nhiên (text/voice) và trả về ảnh – video – audio có ngữ nghĩa tương đồng.

---

##  Mục tiêu dự án

1. Phát triển **MVP hoàn chỉnh** gồm 3 module chính:
   - **Giao diện người dùng:** Nhập truy vấn (text/voice), hiển thị kết quả multimedia.  
   - **Trợ lý ảo điều phối:** Hỗ trợ truy vấn chưa rõ, gợi ý thêm ngữ cảnh.  
   - **Tìm kiếm đa phương tiện:** Sử dụng semantic search qua CLIP + Milvus.  

2. **Dữ liệu demo:**
   - Kho dữ liệu gồm ảnh/video/audio gắn nhãn.
   - Metadata quản lý bằng `metadata.json` hoặc `index.pkl`.

3. **Demo hoàn chỉnh:**
   - Giao diện trực quan, phản hồi nhanh.
   - Có báo cáo kỹ thuật, hướng dẫn chạy trên cloud.

---

##  Kiến trúc hệ thống

### Tổng quan
```
User Query → Text/Voice → Google Translate API → Vector Query → Milvus Search → Retrieve Results → Streamlit UI
```

### Quy trình chính
1. **Xử lý dữ liệu video:**  
   - Trích xuất *keyframes* bằng OpenCV.  
   - Sinh vector embedding cho ảnh/video/audio qua CLIP.  
   - Lưu vào **Milvus** và metadata vào **PostgreSQL**.  

2. **Xử lý truy vấn:**  
   - Người dùng nhập văn bản / ảnh → chuyển thành vector embedding.  
   - Tìm kiếm Top-K kết quả tương tự bằng **cosine similarity** trong Milvus.  

3. **Hiển thị kết quả:**  
   - Giao diện Streamlit hiển thị video/ảnh/audio kèm thông tin chi tiết.  
   - Cho phép refine search, lọc lại kết quả theo tag/ngữ nghĩa.

---

##  Công nghệ chính

| Thành phần | Công cụ / Framework | Ghi chú |
|-------------|--------------------|---------|
| **Vector DB** | Milvus v2.4.1 | Lưu trữ & tìm kiếm vector |
| **Embedding Model** | CLIP / BLIP-2 | Sinh vector từ text + ảnh |
| **Dịch & xử lý tiếng Việt** | Google Translate API, VnCoreNLP | Chuẩn hóa truy vấn |
| **Web App** | Streamlit / Gradio | Giao diện trực quan, dễ deploy |
| **Database** | PostgreSQL 15 | Quản lý metadata |
| **Containerization** | Docker + docker-compose | Tự động hoá môi trường |
| **Hosting** | Google Cloud Platform (GCP) | VM Ubuntu 25.04 (32GB RAM, SSD+HDD) |

---

##  Hạ tầng Cloud

**Nền tảng:** Google Cloud Compute Engine  

**Cấu hình máy chủ:**
- 8 vCPU Intel® Xeon®  
- 32GB RAM  
- 250GB SSD (chạy hệ thống)  
- 280GB HDD (lưu dữ liệu embedding + media)  
- OS: Ubuntu 25.04 (64-bit, Kernel 6.14.0-gcp)

> Tất cả các thành viên đều có user riêng để SSH vào và thao tác trên máy chủ.

---

###  Thiết lập môi trường ban đầu

```bash
# Cập nhật & cài đặt cơ bản
sudo apt update && sudo apt upgrade -y
sudo apt install docker.io docker-compose python3-venv git -y
```

###  Tạo user & phân quyền trên Linux

```bash
# Tạo user riêng cho từng thành viên
sudo adduser thuan
sudo adduser huy
sudo adduser an

# Phân quyền thư mục project + data
sudo mkdir -p /home/ubuntu/AI_CHALLENGE_HTTA/data/batch1
sudo mkdir -p /home/ubuntu/AI_CHALLENGE_HTTA/data/batch2

sudo chown -R tai:htta /home/ubuntu/AI_CHALLENGE_HTTA
sudo usermod -aG docker thuan
sudo usermod -aG docker huy
sudo usermod -aG docker an
```

---

##  Cấu trúc thư mục

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
├── app.py                     # Main app Streamlit
├── docker-compose.yml         # Chạy Milvus + Postgres
├── requirements.txt           # Thư viện Python
├── README.md                  # File mô tả dự án
├── note_to_run_app.txt        # Ghi chú kỹ thuật
├── venv/                      # Virtual environment
└── data/                      # Lưu embedding & media
```

---

##  Hướng dẫn chạy hệ thống

```bash
# 1. Clone repo
git clone https://github.com/HTTA-Legends/AI_CHALLENGE_HTTA.git
cd AI_CHALLENGE_HTTA

# 2. Tạo môi trường ảo
python3 -m venv venv
source venv/bin/activate

# 3. Cài thư viện
pip install -r requirements.txt

# 4. Chạy Docker services
docker-compose up -d

# 5. Chạy giao diện web (Streamlit)
streamlit run app.py
```

> (Ảnh giao diện demo sẽ được thêm tại đây)

---

##  Phân công & Vai trò
| Thành viên | Vai trò | Công việc | Công nghệ chính |
|-------------|----------|------------|----------------|
| **Vỏ Văn Tài** | Leader /Data Engineer | Thiết lập Cloud (GCP), cấu hình Linux, xây dựng giao diện & CLIP model, tích hợp pipeline,tối ưu truy vấn Milvus | Docker, Python, Streamlit, CLIP ,Milvus|
| **Nguyễn Hoàng Ân** | NLP Engineer | Xử lý tiếng Việt, tích hợp Google Translate API, chuẩn hóa truy vấn | HuggingFace, VnCoreNLP |
| **Phan Nguyễn Vũ Huy** | Vision Engineer | Xây dựng mô-đun tìm kiếm ảnh/video/audio, tối ưu truy vấn Milvus | PyTorch, OpenCV, Milvus |
| **Huỳnh Chí Phi Thuận** | Data Engineer / Backend | Xây dựng hệ thống upload vector, quản lý metadata, tạo database, tối ưu truy vấn Milvus| PostgreSQL, Docker,Milvus |

---

## Điểm nổi bật

- **CLIP + Milvus:** Tìm kiếm hình ảnh theo ngữ nghĩa, không cần huấn luyện lại.  
- **Triển khai thực tế trên GCP Ubuntu**, phân quyền Linux cho từng user.  
- **Kiến trúc Docker hóa**, dễ mở rộng và tái tạo môi trường.  
- **Hỗ trợ truy vấn tiếng Việt** và dịch tự động qua API.  

---
Kỹ năng nhóm học được
Nhóm kỹ năng	Mô tả chi tiết
AI/ML Systems	Semantic Search, CLIP embeddings, BLIP-2, RAG architecture
Data Engineering	Preprocessing, metadata schema, PostgreSQL integration
DevOps & Cloud	Google Cloud setup, Docker Compose, Linux permission control
Web & Visualization	Streamlit UI, API interaction, multimedia rendering
Collaboration	GitHub workflow, phân quyền hệ thống, teamwork hiệu quả

##  Tài liệu tham khảo

### 🔗 Nguồn chính thức & hướng dẫn
- [AI Challenge 2025 – Website chính thức](https://aichallenge.hochiminhcity.gov.vn/)  
- [Video Browser Showdown 2024 Systems](https://videobrowsershowdown.org/teams/vbs2024-systems/)  
- [CLIP Model Documentation – HuggingFace](https://huggingface.co/docs/transformers/model_doc/clip)  
- [RAG Chatbot Architecture – CSC Vietnam](https://csc.edu.vn/tin-tuc/Blog-chia-se/kham-pha-rag-huong-dan-xay-dung-chatbot-voi-rag-8433)  
- [Vector DB Comparison – RealPython](https://realpython.com/chromadb-vector-database/)
- Radford, A. *et al.* (2021). [Learning Transferable Visual Models From Natural Language Supervision (CLIP)](https://arxiv.org/abs/2103.00020). *arXiv preprint arXiv:2103.00020.*  
- Li, J. *et al.* (2023). [BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models](https://arxiv.org/abs/2301.12597). *arXiv.*  
- Milvus Team. (2022). [Vector Database for AI Applications](https://milvus.io/blog). *Zilliz Tech.*  
- Zhang, Y. *et al.* (2022). *Efficient Semantic Search with Vector Databases.* *ACM Multimedia Conference.*  
- Nguyen, H. *et al.* (2020). *VnCoreNLP: A Vietnamese Natural Language Processing Toolkit.* *Proceedings of the 12th Language Resources and Evaluation Conference (LREC 2020).*

---

##  Demo & Video trình diễn
 [Xem video demo trên YouTube](https://youtu.be/your_demo_link)

##  Liên hệ
**Vỏ Văn Tài** – Data Engineer / AI Developer  
 Email: vovantai2k4@gmail.com

##  Ghi chú
Nếu bạn thấy dự án này thú vị, hãy ** Star** repo để ủng hộ team HTTA Legends!


