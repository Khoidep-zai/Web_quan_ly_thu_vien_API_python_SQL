# 🔧 Sửa lỗi "no such table: users"

## ❌ Lỗi bạn gặp:
```
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table: users
```

## ✅ Giải pháp nhanh nhất:

### Cách 1: Dùng script tự động (Khuyến nghị)

```powershell
# Đảm bảo đã kích hoạt virtual environment
.\.venv\Scripts\Activate.ps1

# Chạy script khởi tạo database
python init_database.py
```

Script này sẽ tự động:
- Tạo tất cả các bảng cần thiết
- Kiểm tra xem đã có admin chưa
- Hướng dẫn các bước tiếp theo

---

### Cách 2: Dùng Flask Migrate (Chuẩn)

```powershell
# 1. Đảm bảo đã kích hoạt virtual environment
.\.venv\Scripts\Activate.ps1

# 2. Thiết lập biến môi trường
$env:FLASK_APP = "src.app:create_app"

# 3. Khởi tạo migrations (nếu chưa có)
flask db init

# 4. Tạo migration
flask db migrate -m "Initial migration"

# 5. Áp dụng migration để tạo bảng
flask db upgrade
```

---

### Cách 3: Tạo bảng trực tiếp (Nhanh nhất)

```powershell
# Đảm bảo đã kích hoạt virtual environment
.\.venv\Scripts\Activate.ps1

# Chạy Python và tạo bảng
python -c "from src.app import create_app; from src.extensions import db; app = create_app(); app.app_context().push(); db.create_all(); print('✅ Đã tạo các bảng thành công!')"
```

---

## 🔍 Kiểm tra database đã được tạo chưa:

```powershell
# Kiểm tra file database (nếu dùng SQLite)
Test-Path library.db

# Nếu có file, xem kích thước
Get-Item library.db | Select-Object Name, Length
```

---

## ⚠️ Nếu vẫn lỗi:

### Bước 1: Xóa database cũ và tạo lại

```powershell
# Xóa file database cũ (nếu có)
Remove-Item library.db -ErrorAction SilentlyContinue

# Xóa thư mục migrations (nếu có)
Remove-Item -Recurse -Force migrations -ErrorAction SilentlyContinue

# Tạo lại từ đầu
python init_database.py
```

### Bước 2: Kiểm tra cấu hình database

Kiểm tra file `src/config.py` - đảm bảo đường dẫn database đúng.

Nếu dùng SQLite, file `library.db` sẽ được tạo trong thư mục dự án.

### Bước 3: Kiểm tra quyền ghi file

Đảm bảo bạn có quyền ghi file trong thư mục dự án.

---

## ✅ Sau khi sửa xong:

1. **Tạo tài khoản admin** (nếu chưa có):
   ```powershell
   python create_admin.py
   ```

2. **Chạy ứng dụng**:
   ```powershell
   python run.py
   ```

3. **Truy cập**: http://localhost:5000

---

## 📝 Lưu ý:

- **Lần đầu chạy** phải khởi tạo database trước
- **Không xóa database** nếu đã có dữ liệu (sẽ mất hết dữ liệu)
- **Backup database** trước khi xóa: `Copy-Item library.db library.db.backup`

---

## 🎯 Tóm tắt các lệnh:

```powershell
# 1. Kích hoạt venv
.\.venv\Scripts\Activate.ps1

# 2. Khởi tạo database (chọn 1 trong 3 cách)
python init_database.py          # Cách 1: Tự động
# HOẶC
flask db upgrade                 # Cách 2: Migrate
# HOẶC
python -c "from src.app import create_app; from src.extensions import db; app = create_app(); app.app_context().push(); db.create_all()"

# 3. Tạo admin
python create_admin.py

# 4. Chạy web
python run.py
```

