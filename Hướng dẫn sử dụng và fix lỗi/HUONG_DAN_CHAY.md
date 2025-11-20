# 📖 Hướng dẫn chạy Web - Hệ thống quản lý thư viện

## 🚀 Các bước chạy web (Windows PowerShell)

### Bước 1: Mở PowerShell và di chuyển đến thư mục dự án

```powershell
cd "C:\O E\Python nâng cao\ĐỒ ÁN"
```

### Bước 2: Tạo và kích hoạt Virtual Environment

```powershell
# Tạo virtual environment
python -m venv .venv

# Kích hoạt virtual environment
.\.venv\Scripts\Activate.ps1
```

**Lưu ý**: Sau khi kích hoạt, bạn sẽ thấy `(.venv)` ở đầu dòng lệnh.

### Bước 3: Cài đặt các thư viện cần thiết

```powershell
pip install -r requirements.txt
```

Quá trình này có thể mất vài phút để tải và cài đặt tất cả các package.

### Bước 4: Thiết lập biến môi trường (Tùy chọn)

Nếu bạn muốn sử dụng PostgreSQL, tạo file `.env`:

```powershell
# Copy file mẫu
copy .env.example .env

# Mở file .env và chỉnh sửa nếu cần
notepad .env
```

**Lưu ý**: Nếu không có PostgreSQL, hệ thống sẽ tự động sử dụng SQLite (không cần cấu hình gì thêm).

### Bước 5: Khởi tạo Database

```powershell
# Thiết lập biến môi trường Flask
$env:FLASK_APP = "src.app:create_app"
$env:FLASK_ENV = "development"

# Khởi tạo migrations
flask db init

# Tạo migration đầu tiên
flask db migrate -m "Initial migration"

# Áp dụng migration để tạo database
flask db upgrade
```

**Lưu ý**: 
- Lần đầu chạy sẽ tạo thư mục `migrations/` và file database
- Nếu dùng SQLite, file `library.db` sẽ được tạo tự động

### Bước 6: Tạo tài khoản Admin (Quan trọng!)

```powershell
python create_admin.py
```

Nhập thông tin khi được yêu cầu:
- Email admin (ví dụ: `admin@library.com`)
- Tên admin (ví dụ: `Administrator`)
- Mật khẩu (ví dụ: `admin123`)

**Lưu ý**: Bạn cần tài khoản admin để quản lý sách và xem thống kê.

### Bước 7: Chạy ứng dụng Web

Có 2 cách để chạy:

#### Cách 1: Sử dụng run.py (Đơn giản nhất)

```powershell
python run.py
```

#### Cách 2: Sử dụng Flask CLI

```powershell
flask run
```

### Bước 8: Mở trình duyệt

Sau khi chạy thành công, bạn sẽ thấy thông báo:
```
 * Running on http://127.0.0.1:5000
```

Mở trình duyệt và truy cập:
- **URL**: http://localhost:5000 hoặc http://127.0.0.1:5000

## ✅ Kiểm tra hệ thống hoạt động

1. **Trang chủ**: Bạn sẽ thấy giao diện chào mừng
2. **Đăng ký**: Tạo tài khoản user mới
3. **Đăng nhập**: Đăng nhập bằng tài khoản admin hoặc user vừa tạo
4. **Dashboard**: Sau khi đăng nhập, bạn sẽ thấy dashboard

## 🎯 Sử dụng lần đầu

### Đăng nhập với tài khoản Admin:
- Email: (email bạn đã nhập ở bước 6)
- Mật khẩu: (mật khẩu bạn đã nhập ở bước 6)

### Thêm sách đầu tiên:
1. Đăng nhập với tài khoản admin
2. Vào menu "Quản lý" > "Thêm sách"
3. Điền thông tin sách và lưu

### Mượn sách:
1. Vào "Danh sách sách"
2. Chọn sách muốn mượn
3. Click nút "Mượn sách"

## ⚠️ Xử lý lỗi thường gặp

### Lỗi: "ModuleNotFoundError"
```powershell
# Đảm bảo đã kích hoạt virtual environment
.\.venv\Scripts\Activate.ps1

# Cài đặt lại dependencies
pip install -r requirements.txt
```

### Lỗi: "flask: command not found"
```powershell
# Đảm bảo đã thiết lập biến môi trường
$env:FLASK_APP = "src.app:create_app"
```

### Lỗi: "Port already in use"
```powershell
# Thay đổi port trong run.py hoặc dùng:
flask run --port 5001
```

### Lỗi kết nối database
- Nếu dùng PostgreSQL: Kiểm tra PostgreSQL đang chạy và thông tin trong `.env`
- Nếu dùng SQLite: Đảm bảo có quyền ghi file trong thư mục dự án

## 📝 Lưu ý quan trọng

1. **Luôn kích hoạt virtual environment** trước khi chạy:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

2. **Lần đầu chạy** phải thực hiện đầy đủ các bước từ 1-7

3. **Các lần chạy sau** chỉ cần:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   python run.py
   ```

4. **Tắt server**: Nhấn `Ctrl + C` trong PowerShell

## 🎉 Hoàn thành!

Nếu bạn thấy trang web hiển thị bình thường, bạn đã chạy thành công! 

Bây giờ bạn có thể:
- ✅ Đăng ký/Đăng nhập
- ✅ Thêm sách (admin)
- ✅ Mượn/Trả sách
- ✅ Xem thống kê
- ✅ Xuất báo cáo PDF

---

**Cần trợ giúp?** Xem thêm trong file `SETUP.md` hoặc `README.md`

