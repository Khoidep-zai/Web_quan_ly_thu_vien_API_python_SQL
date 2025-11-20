# Hướng dẫn thiết lập và chạy hệ thống quản lý thư viện

## Yêu cầu hệ thống

- Python 3.8 trở lên
- PostgreSQL (hoặc SQLite cho development)
- pip (Python package manager)

## Cài đặt

### 1. Tạo virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Cài đặt dependencies

```powershell
pip install -r requirements.txt
```

### 3. Cấu hình môi trường

Tạo file `.env` từ `.env.example` và điền thông tin:

```powershell
# Copy file mẫu
copy .env.example .env

# Chỉnh sửa .env với thông tin của bạn
```

**Lưu ý quan trọng:**
- Nếu không có PostgreSQL, hệ thống sẽ tự động sử dụng SQLite (file `library.db` sẽ được tạo tự động)
- Để gửi email nhắc nhở, cần cấu hình SMTP (Gmail, Outlook, etc.)

### 4. Khởi tạo database

```powershell
# Thiết lập biến môi trường
$env:FLASK_APP = "src.app:create_app"
$env:FLASK_ENV = "development"

# Tạo database và migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 5. Tạo tài khoản admin (tùy chọn)

Chạy script Python để tạo admin:

```powershell
python -c "from src.app import create_app; from src.models import User, db; app = create_app(); app.app_context().push(); admin = User(email='admin@example.com', name='Admin', is_admin=True); admin.set_password('admin123'); db.session.add(admin); db.session.commit(); print('Admin created!')"
```

Hoặc đăng ký tài khoản thường, sau đó vào database và set `is_admin = True` cho user đó.

## Chạy ứng dụng

### Cách 1: Sử dụng Flask CLI

```powershell
flask run
```

### Cách 2: Sử dụng run.py

```powershell
python run.py
```

Ứng dụng sẽ chạy tại: http://localhost:5000

## Tính năng chính

### Cho người dùng thường:
- Đăng ký/Đăng nhập
- Tìm kiếm sách (theo tên, tác giả, thể loại, ISBN)
- Mượn sách
- Trả sách
- Đặt trước sách đang được mượn
- Xem dashboard cá nhân
- Xem lịch sử mượn

### Cho Admin:
- Tất cả tính năng của user
- Quản lý sách (thêm, sửa, xóa)
- Quản lý mượn/trả
- Quản lý đặt trước
- Dashboard thống kê:
  - Tổng số sách, độc giả
  - Sách đang mượn, quá hạn
  - Top 10 sách mượn nhiều nhất
  - Top 10 độc giả tích cực
  - Thống kê theo tháng
- Xuất báo cáo PDF:
  - Báo cáo mượn/trả
  - Báo cáo danh sách sách
  - Báo cáo thống kê

## RESTful API

Hệ thống cung cấp các API endpoints:

### Sách
- `GET /books/api` - Danh sách sách
- `GET /books/api/<id>` - Chi tiết sách
- `POST /books/api` - Tạo sách mới (admin)
- `PUT /books/api/<id>` - Cập nhật sách (admin)
- `DELETE /books/api/<id>` - Xóa sách (admin)

### Mượn/Trả
- `POST /loans/api/borrow/<book_id>` - Mượn sách
- `POST /loans/api/return/<borrow_id>` - Trả sách

### Đặt trước
- `POST /reservations/api/reserve/<book_id>` - Đặt trước sách

### Thống kê
- `GET /dashboard/api/stats` - Thống kê tổng quan (admin)

## Email nhắc nhở

Hệ thống tự động gửi email:
- **Nhắc nhở trả sách**: 3 ngày trước hạn trả (9:00 AM hàng ngày)
- **Cảnh báo quá hạn**: Hàng ngày cho sách đã quá hạn (9:30 AM)

**Lưu ý**: Cần cấu hình SMTP trong file `.env` để tính năng này hoạt động.

## Phí trễ hạn

Mặc định: 0.5 VNĐ/ngày. Có thể thay đổi trong file `.env`:
```
FINE_PER_DAY=0.5
```

## Troubleshooting

### Lỗi kết nối database
- Kiểm tra `DATABASE_URL` trong `.env`
- Đảm bảo PostgreSQL đang chạy (nếu dùng PostgreSQL)
- Hoặc để trống để dùng SQLite

### Lỗi gửi email
- Kiểm tra cấu hình SMTP trong `.env`
- Với Gmail, cần sử dụng "App Password" thay vì mật khẩu thường
- Có thể tắt tính năng email bằng cách không cấu hình `MAIL_USERNAME`

### Lỗi import
- Đảm bảo đã activate virtual environment
- Chạy `pip install -r requirements.txt` lại

## Phát triển thêm

- Thêm tính năng đánh giá sách
- Thêm tính năng comment/review
- Tích hợp thanh toán online
- Thêm API authentication (JWT)
- Thêm tính năng export Excel
- Thêm tính năng thông báo push notification

