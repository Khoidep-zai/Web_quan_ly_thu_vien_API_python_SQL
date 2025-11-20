# 🔧 Hướng dẫn xử lý lỗi thường gặp

## ❌ Các lỗi phổ biến và cách khắc phục

### 1. Lỗi: "ModuleNotFoundError" hoặc "No module named 'src'"

**Nguyên nhân**: Python không tìm thấy module hoặc chưa kích hoạt virtual environment

**Giải pháp**:
```powershell
# Đảm bảo đã kích hoạt virtual environment
.\.venv\Scripts\Activate.ps1

# Kiểm tra Python đang dùng
python --version
which python  # hoặc: where python

# Cài đặt lại dependencies
pip install -r requirements.txt
```

---

### 2. Lỗi: "flask: command not found" hoặc "flask db: command not found"

**Nguyên nhân**: Chưa thiết lập biến môi trường FLASK_APP

**Giải pháp**:
```powershell
$env:FLASK_APP = "src.app:create_app"
flask db init
```

Hoặc sử dụng trực tiếp:
```powershell
python run.py
```

---

### 3. Lỗi: "Table 'users' already exists" hoặc lỗi migration

**Nguyên nhân**: Database đã được tạo nhưng migration bị lỗi

**Giải pháp**:
```powershell
# Xóa database cũ (nếu dùng SQLite)
Remove-Item library.db -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force migrations -ErrorAction SilentlyContinue

# Tạo lại từ đầu
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

---

### 4. Lỗi: "Address already in use" hoặc "Port 5000 already in use"

**Nguyên nhân**: Port 5000 đang được sử dụng bởi ứng dụng khác

**Giải pháp**:
```powershell
# Cách 1: Tìm và tắt process đang dùng port 5000
netstat -ano | findstr :5000
# Lấy PID và kill process đó
taskkill /PID <PID> /F

# Cách 2: Đổi port trong run.py
# Sửa dòng: app.run(debug=True, host='0.0.0.0', port=5001)

# Cách 3: Dùng Flask CLI với port khác
flask run --port 5001
```

---

### 5. Lỗi: "ImportError: cannot import name 'create_app'" hoặc lỗi import

**Nguyên nhân**: Cấu trúc thư mục hoặc import path không đúng

**Giải pháp**:
```powershell
# Đảm bảo đang ở đúng thư mục dự án
cd "C:\O E\Python nâng cao\ĐỒ ÁN"

# Kiểm tra file src/app.py có tồn tại
Test-Path src/app.py

# Chạy từ thư mục gốc
python run.py
```

---

### 6. Lỗi: "TemplateNotFound" hoặc "jinja2.exceptions.TemplateNotFound"

**Nguyên nhân**: Template file không tồn tại hoặc đường dẫn sai

**Giải pháp**:
```powershell
# Kiểm tra thư mục templates
Test-Path src/templates/index.html

# Đảm bảo cấu trúc thư mục đúng:
# src/templates/
#   - base.html
#   - index.html
#   - auth/login.html
#   - auth/register.html
#   - books/list.html
#   ...
```

---

### 7. Lỗi: "RuntimeError: Working outside of application context"

**Nguyên nhân**: Cố gắng truy cập Flask context bên ngoài app context

**Giải pháp**: Đảm bảo code chạy trong app context:
```python
# Trong create_admin.py hoặc script khác
with app.app_context():
    # Code của bạn ở đây
    pass
```

---

### 8. Lỗi: "Scheduler already running" hoặc lỗi scheduler

**Nguyên nhân**: Scheduler đã được start nhiều lần

**Giải pháp**: Sửa file `src/app.py`:
```python
# Thay vì:
scheduler.init_app(app)
scheduler.start()

# Sửa thành:
scheduler.init_app(app)
if not scheduler.running:
    scheduler.start()
```

---

### 9. Lỗi: "OperationalError: no such table" hoặc lỗi database

**Nguyên nhân**: Database chưa được tạo hoặc migration chưa chạy

**Giải pháp**:
```powershell
# Chạy migrations
flask db upgrade

# Nếu vẫn lỗi, tạo lại database
flask db init
flask db migrate -m "Recreate database"
flask db upgrade
```

---

### 10. Lỗi: "psycopg2" hoặc lỗi PostgreSQL

**Nguyên nhân**: Không có PostgreSQL hoặc cấu hình sai

**Giải pháp**:
- **Cách 1**: Cài đặt PostgreSQL và cấu hình trong `.env`
- **Cách 2**: Xóa `DATABASE_URL` trong `.env` để dùng SQLite (tự động)

```powershell
# Xóa hoặc comment dòng DATABASE_URL trong .env
# Hệ thống sẽ tự động dùng SQLite
```

---

### 11. Lỗi: "AttributeError: 'NoneType' object has no attribute..."

**Nguyên nhân**: Object không tồn tại trong database

**Giải pháp**: Kiểm tra xem đã tạo dữ liệu mẫu chưa:
```powershell
# Tạo admin account
python create_admin.py

# Hoặc tạo dữ liệu mẫu trong Python shell
python
>>> from src.app import create_app
>>> from src.models import Book, db
>>> app = create_app()
>>> with app.app_context():
...     book = Book(title="Sách mẫu", author="Tác giả", total_copies=5)
...     db.session.add(book)
...     db.session.commit()
```

---

### 12. Lỗi khi chạy `python create_admin.py`

**Nguyên nhân**: Database chưa được tạo

**Giải pháp**:
```powershell
# Chạy migrations trước
flask db upgrade

# Sau đó mới chạy create_admin.py
python create_admin.py
```

---

## 🔍 Cách kiểm tra lỗi chi tiết

### Xem log lỗi đầy đủ:
```powershell
# Chạy với debug mode
python run.py

# Hoặc set FLASK_DEBUG
$env:FLASK_DEBUG = "1"
python run.py
```

### Kiểm tra Python path:
```powershell
python -c "import sys; print(sys.path)"
```

### Kiểm tra packages đã cài:
```powershell
pip list
```

### Kiểm tra virtual environment:
```powershell
# Xem Python đang dùng
python -c "import sys; print(sys.executable)"

# Phải trỏ đến .venv\Scripts\python.exe
```

---

## ✅ Checklist trước khi chạy

- [ ] Đã kích hoạt virtual environment (`.venv`)
- [ ] Đã cài đặt tất cả dependencies (`pip install -r requirements.txt`)
- [ ] Đã thiết lập `FLASK_APP` (hoặc dùng `python run.py`)
- [ ] Đã chạy migrations (`flask db upgrade`)
- [ ] Đã tạo tài khoản admin (`python create_admin.py`)
- [ ] Đang ở đúng thư mục dự án

---

## 🆘 Vẫn không được?

1. **Xóa và cài lại từ đầu**:
```powershell
# Xóa virtual environment
Remove-Item -Recurse -Force .venv

# Xóa database (nếu dùng SQLite)
Remove-Item library.db -ErrorAction SilentlyContinue

# Tạo lại từ đầu theo hướng dẫn
```

2. **Kiểm tra Python version** (phải >= 3.8):
```powershell
python --version
```

3. **Cập nhật pip**:
```powershell
python -m pip install --upgrade pip
```

4. **Chạy với quyền Administrator** (nếu cần)

---

**Nếu vẫn gặp lỗi, vui lòng cung cấp:**
- Thông báo lỗi đầy đủ (copy/paste)
- Lệnh bạn đang chạy
- Python version (`python --version`)
- Đã làm những bước nào trước đó

