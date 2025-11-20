# ⚡ Quick Start - Docker

Hướng dẫn nhanh để chạy đồ án với Docker trong 3 bước!

## 🚀 3 Bước đơn giản:

### 1. Mở PowerShell trong thư mục dự án

```powershell
cd "C:\O E\Python nâng cao\ĐỒ ÁN"
```

### 2. Chạy Docker Compose

```powershell
docker-compose up -d --build
```

Lần đầu sẽ mất vài phút để download images. Các lần sau sẽ nhanh hơn!

### 3. Truy cập ứng dụng

Mở trình duyệt: **http://localhost:5000**

---

## ✅ Xong rồi!

Bây giờ bạn có thể:
- ✅ Truy cập web tại http://localhost:5000
- ✅ Đăng ký/Đăng nhập
- ✅ Sử dụng tất cả tính năng

---

## 📝 Tạo tài khoản Admin

```powershell
docker-compose exec web python create_admin.py
```

Nhập thông tin khi được yêu cầu.

---

## 🛑 Dừng ứng dụng

```powershell
docker-compose stop
```

Hoặc dừng và xóa containers:

```powershell
docker-compose down
```

---

## 📖 Xem logs

```powershell
docker-compose logs -f
```

---

## 🔄 Restart

```powershell
docker-compose restart
```

---

## ❓ Cần giúp đỡ?

Xem file **DOCKER_GUIDE.md** để biết hướng dẫn chi tiết!

