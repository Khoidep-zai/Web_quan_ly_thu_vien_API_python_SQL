# 📚 HỆ THỐNG QUẢN LÝ THƯ VIỆN TRỰC TUYẾN

> **Mô tả ngắn gọn:** Đây là một website quản lý thư viện, cho phép người dùng mượn sách, trả sách, tìm kiếm sách và quản trị viên có thể quản lý toàn bộ hệ thống.

---

## 📖 MỤC LỤC

1. [Giới thiệu dự án](#-giới-thiệu-dự-án)
2. [Tính năng của hệ thống](#-tính-năng-của-hệ-thống)
3. [Cấu trúc thư mục dự án](#-cấu-trúc-thư-mục-dự-án-giải-thích-chi-tiết)
4. [Hướng dẫn cài đặt](#-hướng-dẫn-cài-đặt-từng-bước)
5. [Hướng dẫn chạy ứng dụng](#-hướng-dẫn-chạy-ứng-dụng)
6. [Hướng dẫn sử dụng Docker](#-hướng-dẫn-sử-dụng-docker-dành-cho-người-mới)
7. [Giải thích các thành phần kỹ thuật](#-giải-thích-các-thành-phần-kỹ-thuật)
8. [Câu hỏi thường gặp](#-câu-hỏi-thường-gặp-faq)

---

## 🎯 GIỚI THIỆU DỰ ÁN

### Dự án này là gì?
Đây là một **website quản lý thư viện** được xây dựng để:
- Giúp **độc giả** (người dùng) có thể tìm kiếm và mượn sách online
- Giúp **thủ thư/quản trị viên** quản lý sách, theo dõi việc mượn trả

### Công nghệ sử dụng (giải thích đơn giản)

| Công nghệ | Vai trò | Giải thích dễ hiểu |
|-----------|---------|-------------------|
| **Python** | Ngôn ngữ lập trình | Ngôn ngữ để viết code cho website |
| **Flask** | Framework web | Bộ công cụ giúp tạo website dễ dàng hơn |
| **SQLite/PostgreSQL** | Cơ sở dữ liệu | Nơi lưu trữ thông tin sách, người dùng |
| **Bootstrap** | Giao diện | Giúp website đẹp và hiển thị tốt trên điện thoại |
| **Docker** | Đóng gói ứng dụng | Giúp chạy website ở bất kỳ máy nào mà không cần cài đặt phức tạp |

---

## ✨ TÍNH NĂNG CỦA HỆ THỐNG

### 👤 Dành cho NGƯỜI DÙNG (Độc giả)

| Tính năng | Mô tả |
|-----------|-------|
| 📝 Đăng ký/Đăng nhập | Tạo tài khoản và đăng nhập vào hệ thống |
| 🔍 Tìm kiếm sách | Tìm sách theo tên, tác giả, thể loại hoặc mã ISBN |
| 📖 Mượn sách | Mượn sách với thời hạn 14 ngày |
| ↩️ Trả sách | Trả sách và xem tiền phạt (nếu trễ hạn) |
| 📅 Đặt trước sách | Đặt trước khi sách đang được người khác mượn |
| 📊 Xem lịch sử | Xem lịch sử các sách đã mượn |

### 👑 Dành cho ADMIN (Quản trị viên)

| Tính năng | Mô tả |
|-----------|-------|
| 📚 Quản lý sách | Thêm sách mới, sửa thông tin, xóa sách |
| 👥 Quản lý mượn/trả | Xem tất cả giao dịch mượn trả trong hệ thống |
| 📈 Thống kê | Xem báo cáo: sách mượn nhiều nhất, độc giả tích cực... |
| 📄 Xuất PDF | Xuất báo cáo ra file PDF |

### 🤖 Tính năng TỰ ĐỘNG

| Tính năng | Mô tả |
|-----------|-------|
| 📧 Nhắc nhở | Tự động gửi email nhắc trả sách trước 3 ngày |
| ⚠️ Cảnh báo | Tự động gửi email khi sách quá hạn |
| 💰 Tính phạt | Tự động tính tiền phạt khi trả sách trễ |

---

## 📁 CẤU TRÚC THƯ MỤC DỰ ÁN (Giải thích chi tiết)

```
📦 THƯ MỤC GỐC CỦA DỰ ÁN
│
├── 📄 run.py                    ← FILE CHÍNH ĐỂ CHẠY WEBSITE
├── 📄 requirements.txt          ← Danh sách thư viện cần cài đặt
├── 📄 create_admin.py           ← Tạo tài khoản admin đầu tiên
├── 📄 README.md                 ← File hướng dẫn này
│
├── 🐳 DOCKER (Chạy trên container)
│   ├── 📄 Dockerfile            ← Hướng dẫn Docker tạo container
│   ├── 📄 docker-compose.yml    ← Cấu hình chạy nhiều container
│   └── 📄 docker-entrypoint.sh  ← Script khởi động trong Docker
│
├── 📂 src/                      ← THƯ MỤC CHỨA CODE CHÍNH
│   │
│   ├── 📄 app.py                ← Khởi tạo ứng dụng Flask
│   ├── 📄 config.py             ← Cấu hình (database, email, ...)
│   ├── 📄 extensions.py         ← Khởi tạo các công cụ bổ sung
│   ├── 📄 models.py             ← Định nghĩa cấu trúc dữ liệu
│   │
│   ├── 📂 routes/               ← CÁC TRANG WEB (Xử lý yêu cầu)
│   │   ├── 📄 auth.py           ← Trang đăng nhập, đăng ký
│   │   ├── 📄 books.py          ← Trang quản lý sách
│   │   ├── 📄 loans.py          ← Trang mượn/trả sách
│   │   ├── 📄 reservations.py   ← Trang đặt trước sách
│   │   ├── 📄 dashboard.py      ← Trang tổng quan/thống kê
│   │   └── 📄 reports.py        ← Xuất báo cáo PDF
│   │
│   ├── 📂 tasks/                ← CÔNG VIỆC TỰ ĐỘNG
│   │   └── 📄 email_reminders.py ← Gửi email nhắc nhở tự động
│   │
│   └── 📂 templates/            ← GIAO DIỆN WEBSITE (HTML)
│       ├── 📄 base.html         ← Khung chung cho tất cả trang
│       ├── 📄 index.html        ← Trang chủ
│       ├── 📂 auth/             ← Giao diện đăng nhập/đăng ký
│       ├── 📂 books/            ← Giao diện quản lý sách
│       ├── 📂 loans/            ← Giao diện mượn/trả
│       ├── 📂 reservations/     ← Giao diện đặt trước
│       └── 📂 dashboard/        ← Giao diện thống kê
│
├── 📂 static/                   ← TÀI NGUYÊN TĨNH
│   └── 📂 uploads/books/        ← Lưu ảnh bìa sách
│
├── 📂 docs/                     ← TÀI LIỆU DỰ ÁN
│   └── 📄 structure.md          ← Mô tả cấu trúc chi tiết
│
└── 📂 Hướng dẫn sử dụng.../     ← CÁC FILE HƯỚNG DẪN
    ├── 📄 SETUP.md              ← Hướng dẫn cài đặt
    ├── 📄 DOCKER_GUIDE.md       ← Hướng dẫn Docker
    ├── 📄 HUONG_DAN_CHAY.md     ← Hướng dẫn chạy
    └── 📄 XU_LY_LOI.md          ← Cách xử lý lỗi
```

### 📝 Giải thích từng phần:

#### 1️⃣ **src/** - Thư mục code chính
Đây là "trái tim" của dự án, chứa toàn bộ logic hoạt động.

#### 2️⃣ **src/routes/** - Các trang web
Mỗi file tương ứng với một nhóm trang:
- `auth.py` → Xử lý đăng nhập, đăng ký, đăng xuất
- `books.py` → Xử lý thêm/sửa/xóa/tìm sách
- `loans.py` → Xử lý mượn sách, trả sách
- ...

#### 3️⃣ **src/templates/** - Giao diện
Chứa các file HTML hiển thị cho người dùng xem.

#### 4️⃣ **src/models.py** - Cấu trúc dữ liệu
Định nghĩa các "bảng" trong cơ sở dữ liệu:
- **User** (Người dùng): email, tên, mật khẩu, quyền admin
- **Book** (Sách): tên sách, tác giả, thể loại, số lượng
- **BorrowRecord** (Phiếu mượn): ai mượn, sách gì, ngày mượn, ngày trả
- **Reservation** (Đặt trước): ai đặt, sách gì, ngày đặt

---

## 🚀 HƯỚNG DẪN CÀI ĐẶT (Từng bước)

### Bước 1: Cài đặt Python
- Tải Python từ: https://www.python.org/downloads/
- Khi cài, **nhớ tick vào "Add Python to PATH"**

### Bước 2: Mở thư mục dự án
```powershell
cd "c:\O E\Python nâng cao\ĐỒ ÁN"
```

### Bước 3: Tạo môi trường ảo (Virtual Environment)
```powershell
# Tạo môi trường ảo
python -m venv .venv

# Kích hoạt môi trường ảo
.\.venv\Scripts\Activate.ps1
```
> 💡 **Môi trường ảo là gì?** Là một "phòng riêng" để cài thư viện, không ảnh hưởng đến các dự án khác.

### Bước 4: Cài đặt các thư viện cần thiết
```powershell
pip install -r requirements.txt
```

### Bước 5: Tạo tài khoản Admin
```powershell
python create_admin.py
```
Làm theo hướng dẫn trên màn hình để nhập email và mật khẩu.

---

## ▶️ HƯỚNG DẪN CHẠY ỨNG DỤNG

### Cách 1: Chạy đơn giản nhất
```powershell
python run.py
```

### Cách 2: Sử dụng Flask
```powershell
$env:FLASK_APP = "run.py"
flask run
```

### Sau khi chạy:
1. Mở trình duyệt web (Chrome, Firefox, Edge...)
2. Truy cập địa chỉ: **http://localhost:5000**
3. Đăng nhập bằng tài khoản admin đã tạo

### Để dừng ứng dụng:
Nhấn `Ctrl + C` trong terminal

---

## 🐳 HƯỚNG DẪN SỬ DỤNG DOCKER (Dành cho người mới)

### Docker là gì?
Docker giống như một "hộp đóng gói" chứa sẵn mọi thứ cần thiết để chạy ứng dụng. Bạn chỉ cần chạy 1 lệnh là xong, không cần cài đặt gì thêm.

### Cách 1: Chạy từ Docker Hub (Dễ nhất)
```bash
docker run -p 5000:5000 khoidepzai/web-flask:v1
```
Sau đó mở trình duyệt và vào: **http://localhost:5000**

### Cách 2: Tự build từ source code
```bash
# Build image
docker build -t my-flask-api .

# Chạy container
docker run -p 5000:5000 my-flask-api
```

### Tạo tài khoản Admin trong Docker

**Bước 1:** Xem danh sách container đang chạy
```bash
docker ps
```
Kết quả sẽ hiện tên container, ví dụ: `lucid_khorana`

**Bước 2:** Truy cập vào container
```bash
docker exec -it lucid_khorana bash
```

**Bước 3:** Chạy lệnh tạo admin
```bash
python create_admin.py
```

---

## 🔧 GIẢI THÍCH CÁC THÀNH PHẦN KỸ THUẬT

### 📊 Cơ sở dữ liệu (Database)

Dự án có 4 bảng dữ liệu chính:

```
┌─────────────────────────────────────────────────────────────────┐
│                        CƠ SỞ DỮ LIỆU                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐     │
│  │   USER      │      │    BOOK     │      │ BORROW      │     │
│  │ (Người dùng)│      │   (Sách)    │      │ RECORD      │     │
│  ├─────────────┤      ├─────────────┤      │(Phiếu mượn) │     │
│  │ - ID        │      │ - ID        │      ├─────────────┤     │
│  │ - Email     │◄────►│ - Tên sách  │◄────►│ - ID        │     │
│  │ - Tên       │      │ - Tác giả   │      │ - User ID   │     │
│  │ - Mật khẩu  │      │ - Thể loại  │      │ - Book ID   │     │
│  │ - Là Admin? │      │ - ISBN      │      │ - Ngày mượn │     │
│  └─────────────┘      │ - Số lượng  │      │ - Hạn trả   │     │
│                       │ - Ảnh bìa   │      │ - Đã trả?   │     │
│                       └─────────────┘      │ - Tiền phạt │     │
│                                            └─────────────┘     │
│                                                                 │
│  ┌─────────────────────────────────────────┐                   │
│  │          RESERVATION (Đặt trước)         │                   │
│  ├─────────────────────────────────────────┤                   │
│  │ - ID | User ID | Book ID | Ngày đặt     │                   │
│  └─────────────────────────────────────────┘                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 🔄 Luồng hoạt động của website

```
┌──────────────────────────────────────────────────────────────────┐
│                    CÁCH WEBSITE HOẠT ĐỘNG                        │
└──────────────────────────────────────────────────────────────────┘

    👤 NGƯỜI DÙNG                    🖥️ SERVER                    💾 DATABASE
         │                              │                              │
         │  1. Truy cập website         │                              │
         │  ─────────────────────────►  │                              │
         │                              │                              │
         │                              │  2. Lấy dữ liệu              │
         │                              │  ─────────────────────────►  │
         │                              │                              │
         │                              │  3. Trả về dữ liệu           │
         │                              │  ◄─────────────────────────  │
         │                              │                              │
         │  4. Hiển thị trang web       │                              │
         │  ◄─────────────────────────  │                              │
         │                              │                              │
```

### 🌐 RESTful API (Dành cho lập trình viên)

API cho phép các ứng dụng khác tương tác với hệ thống:

| Phương thức | Đường dẫn | Chức năng |
|-------------|-----------|-----------|
| GET | `/books/api` | Lấy danh sách sách |
| GET | `/books/api/<id>` | Lấy chi tiết 1 sách |
| POST | `/books/api` | Thêm sách mới (Admin) |
| PUT | `/books/api/<id>` | Sửa sách (Admin) |
| DELETE | `/books/api/<id>` | Xóa sách (Admin) |
| POST | `/loans/api/borrow/<id>` | Mượn sách |
| POST | `/loans/api/return/<id>` | Trả sách |

---

## ❓ CÂU HỎI THƯỜNG GẶP (FAQ)

### 1. Làm sao để đổi mật khẩu admin?
Chạy lại lệnh `python create_admin.py` và tạo tài khoản mới.

### 2. Website có thể chạy trên điện thoại không?
Có! Giao diện được thiết kế responsive, hiển thị tốt trên mọi thiết bị.

### 3. Dữ liệu được lưu ở đâu?
- Nếu dùng SQLite: File `library.db` trong thư mục dự án
- Nếu dùng PostgreSQL: Trong database server

### 4. Làm sao để sửa thời hạn mượn sách?
Mở file `.env` và sửa giá trị `BORROW_DAYS_DEFAULT` (mặc định là 14 ngày).

### 5. Tính năng email không hoạt động?
Cần cấu hình thông tin email trong file `.env`:
```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

---

## ⚙️ CẤU HÌNH HỆ THỐNG

Các thiết lập có thể thay đổi trong file `.env`:

| Biến | Mô tả | Giá trị mặc định |
|------|-------|------------------|
| `DATABASE_URL` | Địa chỉ kết nối database | SQLite (tự động) |
| `SECRET_KEY` | Khóa bảo mật | Tự tạo |
| `BORROW_DAYS_DEFAULT` | Số ngày được mượn sách | 14 ngày |
| `REMINDER_DAYS_BEFORE` | Nhắc nhở trước bao nhiêu ngày | 3 ngày |
| `FINE_PER_DAY` | Tiền phạt mỗi ngày trễ | 0.5 VNĐ |

---

## 📞 HỖ TRỢ

Nếu gặp vấn đề, hãy xem các file hướng dẫn trong thư mục `Hướng dẫn sử dụng và fix lỗi/`:
- [SETUP.md](Hướng%20dẫn%20sử%20dụng%20và%20fix%20lỗi/SETUP.md) - Hướng dẫn cài đặt
- [DOCKER_GUIDE.md](Hướng%20dẫn%20sử%20dụng%20và%20fix%20lỗi/DOCKER_GUIDE.md) - Hướng dẫn Docker
- [XU_LY_LOI.md](Hướng%20dẫn%20sử%20dụng%20và%20fix%20lỗi/XU_LY_LOI.md) - Cách xử lý lỗi

---

## 📝 THÔNG TIN DỰ ÁN

- **Mục đích:** Dự án học tập môn Python nâng cao
- **Ngày tạo:** 2025
- **Tác giả:** chủ kênh github

---


