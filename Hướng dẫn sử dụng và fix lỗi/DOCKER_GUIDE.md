# 🐳 Hướng dẫn chạy đồ án với Docker

Hướng dẫn chi tiết để chạy hệ thống quản lý thư viện trên Docker.

## 📋 Yêu cầu

- **Docker** (version 20.10 trở lên)
- **Docker Compose** (version 2.0 trở lên)
- **Git** (để clone repository)

### Kiểm tra cài đặt:

```powershell
docker --version
docker-compose --version
```

Nếu chưa cài, tải tại: https://www.docker.com/products/docker-desktop

---

## 🚀 Cách chạy nhanh

### Bước 1: Clone/Di chuyển đến thư mục dự án

```powershell
cd "C:\O E\Python nâng cao\ĐỒ ÁN"
```

### Bước 2: Tạo file .env (tùy chọn)

Tạo file `.env` trong thư mục dự án để cấu hình:

```env
# Database (đã được cấu hình trong docker-compose.yml)
DATABASE_URL=postgresql://library_user:library_password@db:5432/library_db

# Flask Secret Key (QUAN TRỌNG: đổi trong production!)
SECRET_KEY=your-super-secret-key-change-in-production

# Email (tùy chọn)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com

# Application settings
BORROW_DAYS_DEFAULT=14
REMINDER_DAYS_BEFORE=3
PER_PAGE=20
FINE_PER_DAY=0.5
```

**Lưu ý**: Nếu không tạo file `.env`, hệ thống sẽ dùng giá trị mặc định.

### Bước 3: Build và chạy containers

```powershell
# Build và khởi động tất cả services
docker-compose up -d --build
```

Lệnh này sẽ:
- Build Docker image cho Flask app
- Tạo PostgreSQL container
- Tạo Flask app container
- Tự động chạy migrations
- Khởi tạo database

### Bước 4: Kiểm tra logs

```powershell
# Xem logs của tất cả services
docker-compose logs -f

# Hoặc xem logs của từng service
docker-compose logs -f web
docker-compose logs -f db
```

### Bước 5: Truy cập ứng dụng

Mở trình duyệt và truy cập: **http://localhost:5000**

---

## 📝 Các lệnh Docker thường dùng

### Quản lý containers:

```powershell
# Khởi động containers
docker-compose up -d

# Dừng containers
docker-compose stop

# Dừng và xóa containers
docker-compose down

# Dừng và xóa containers + volumes (XÓA DỮ LIỆU!)
docker-compose down -v

# Xem trạng thái containers
docker-compose ps

# Xem logs
docker-compose logs -f web
```

### Quản lý database:

```powershell
# Chạy migrations
docker-compose exec web flask db upgrade

# Tạo migration mới
docker-compose exec web flask db migrate -m "Migration message"

# Tạo tài khoản admin
docker-compose exec web python create_admin.py

# Truy cập PostgreSQL shell
docker-compose exec db psql -U library_user -d library_db
```

### Rebuild:

```powershell
# Rebuild image (khi thay đổi code)
docker-compose up -d --build

# Rebuild không cache
docker-compose build --no-cache
```

---

## 🔧 Cấu hình nâng cao

### Thay đổi port:

Sửa file `docker-compose.yml`:

```yaml
services:
  web:
    ports:
      - "8080:5000"  # Thay đổi 8080 thành port bạn muốn
```

### Thay đổi database credentials:

Sửa file `docker-compose.yml`:

```yaml
services:
  db:
    environment:
      POSTGRES_USER: your_user
      POSTGRES_PASSWORD: your_password
      POSTGRES_DB: your_database
```

Và cập nhật `DATABASE_URL` trong `.env` hoặc `docker-compose.yml`.

### Thêm environment variables:

Thêm vào file `.env` hoặc trong `docker-compose.yml`:

```yaml
services:
  web:
    environment:
      YOUR_VARIABLE: your_value
```

---

## 🗄️ Quản lý dữ liệu

### Backup database:

```powershell
# Backup PostgreSQL
docker-compose exec db pg_dump -U library_user library_db > backup.sql

# Hoặc backup volume
docker run --rm -v library_postgres_data:/data -v ${PWD}:/backup alpine tar czf /backup/postgres_backup.tar.gz /data
```

### Restore database:

```powershell
# Restore từ file SQL
docker-compose exec -T db psql -U library_user library_db < backup.sql
```

### Xem dữ liệu:

```powershell
# Truy cập PostgreSQL
docker-compose exec db psql -U library_user -d library_db

# Trong PostgreSQL shell:
\dt          # Xem tất cả bảng
SELECT * FROM users;  # Xem dữ liệu
\q           # Thoát
```

---

## 🐛 Xử lý lỗi

### Lỗi: "Port already in use"

```powershell
# Tìm process đang dùng port 5000
netstat -ano | findstr :5000

# Hoặc đổi port trong docker-compose.yml
```

### Lỗi: "Cannot connect to database"

```powershell
# Kiểm tra database container đang chạy
docker-compose ps

# Xem logs database
docker-compose logs db

# Restart database
docker-compose restart db
```

### Lỗi: "Module not found"

```powershell
# Rebuild image
docker-compose build --no-cache
docker-compose up -d
```

### Lỗi: "Permission denied" (Linux/Mac)

```powershell
# Sửa quyền cho thư mục
sudo chown -R $USER:$USER static/uploads
```

### Xóa tất cả và bắt đầu lại:

```powershell
# Dừng và xóa tất cả
docker-compose down -v

# Xóa images
docker rmi library_web

# Build lại từ đầu
docker-compose up -d --build
```

---

## 📦 Cấu trúc Docker

```
.
├── Dockerfile              # Image definition cho Flask app
├── docker-compose.yml      # Orchestration cho tất cả services
├── .dockerignore           # Files/folders bỏ qua khi build
├── .env                    # Environment variables (tùy chọn)
└── ...
```

### Services:

1. **web**: Flask application (port 5000)
2. **db**: PostgreSQL database (port 5432)

### Volumes:

- `postgres_data`: Database data (persistent)
- `./static/uploads`: Uploaded images (persistent)
- `./migrations`: Database migrations (persistent)

---

## 🚀 Production Deployment

### 1. Cập nhật SECRET_KEY:

```env
SECRET_KEY=your-very-long-random-secret-key-here
```

### 2. Cấu hình reverse proxy (Nginx):

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 3. Sử dụng HTTPS:

Cấu hình SSL certificate với Let's Encrypt hoặc Cloudflare.

### 4. Backup tự động:

Thiết lập cron job để backup database định kỳ.

---

## ✅ Checklist trước khi deploy

- [ ] Đã đổi `SECRET_KEY` trong `.env`
- [ ] Đã cấu hình email (nếu cần)
- [ ] Đã tạo tài khoản admin
- [ ] Đã test tất cả tính năng
- [ ] Đã backup database
- [ ] Đã cấu hình firewall/security
- [ ] Đã setup monitoring/logging

---

## 📚 Tài liệu thêm

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [PostgreSQL Docker Image](https://hub.docker.com/_/postgres)

---

## 🆘 Cần trợ giúp?

1. Kiểm tra logs: `docker-compose logs -f`
2. Kiểm tra trạng thái: `docker-compose ps`
3. Xem file hướng dẫn khác trong project
4. Tạo issue trên repository

---

**Lưu ý**: Lần đầu chạy có thể mất vài phút để download images và build. Các lần sau sẽ nhanh hơn nhiều!

