# 🚀 Hướng dẫn đẩy dự án lên GitHub

## 📋 Các bước đẩy dự án lên GitHub repository mới

### Bước 1: Tạo repository mới trên GitHub

1. Đăng nhập GitHub
2. Click nút **"+"** > **"New repository"**
3. Đặt tên repository (ví dụ: `library-management-system`)
4. Chọn **Public** hoặc **Private**
5. **KHÔNG** tích "Initialize with README" (vì đã có code)
6. Click **"Create repository"**

### Bước 2: Thay đổi remote URL

#### Cách 1: Thay đổi remote hiện tại (nếu đã có remote)

```powershell
# Xem remote hiện tại
git remote -v

# Thay đổi URL remote
git remote set-url origin https://github.com/USERNAME/REPOSITORY_NAME.git

# Hoặc nếu dùng SSH
git remote set-url origin git@github.com:USERNAME/REPOSITORY_NAME.git
```

**Thay thế:**
- `USERNAME` = tên GitHub của bạn
- `REPOSITORY_NAME` = tên repository mới bạn vừa tạo

#### Cách 2: Xóa remote cũ và thêm mới

```powershell
# Xóa remote cũ
git remote remove origin

# Thêm remote mới
git remote add origin https://github.com/USERNAME/REPOSITORY_NAME.git
```

### Bước 3: Commit tất cả thay đổi (nếu chưa commit)

```powershell
# Xem file đã thay đổi
git status

# Thêm tất cả file
git add .

# Commit
git commit -m "Hoàn thiện hệ thống quản lý thư viện với upload ảnh và Docker"
```

### Bước 4: Push lên GitHub

```powershell
# Push lên branch main
git push -u origin main

# Hoặc nếu branch của bạn là master
git push -u origin master
```

**Lưu ý:** Lần đầu push cần dùng `-u` để set upstream.

---

## 🔄 Nếu có lỗi "Updates were rejected"

Nếu repository mới đã có file (README, .gitignore, etc.):

```powershell
# Pull trước
git pull origin main --allow-unrelated-histories

# Giải quyết conflict nếu có, sau đó:
git add .
git commit -m "Merge với repository mới"

# Push lại
git push origin main
```

---

## 📝 Ví dụ cụ thể

Giả sử bạn muốn push lên repository: `https://github.com/yourusername/library-management`

```powershell
# 1. Thay đổi remote
git remote set-url origin https://github.com/yourusername/library-management.git

# 2. Kiểm tra
git remote -v

# 3. Commit nếu cần
git add .
git commit -m "Upload dự án hoàn chỉnh"

# 4. Push
git push -u origin main
```

---

## ✅ Kiểm tra kết quả

Sau khi push thành công:
1. Vào GitHub repository của bạn
2. Refresh trang
3. Bạn sẽ thấy tất cả code đã được upload

---

## 🔐 Sử dụng SSH thay vì HTTPS

Nếu muốn dùng SSH (không cần nhập password):

```powershell
# Thay đổi remote sang SSH
git remote set-url origin git@github.com:USERNAME/REPOSITORY_NAME.git

# Push
git push -u origin main
```

**Lưu ý:** Cần setup SSH key trước (xem hướng dẫn GitHub).

---

## 🆘 Xử lý lỗi

### Lỗi: "fatal: remote origin already exists"
```powershell
git remote remove origin
git remote add origin https://github.com/USERNAME/REPO.git
```

### Lỗi: "Authentication failed"
- Kiểm tra username/password
- Hoặc dùng Personal Access Token thay vì password
- Hoặc setup SSH key

### Lỗi: "Permission denied"
- Kiểm tra bạn có quyền truy cập repository
- Kiểm tra repository là Public hoặc bạn được mời vào Private repo

---

## 📦 File nào sẽ được push?

Theo `.gitignore`, các file sau sẽ **KHÔNG** được push:
- ❌ `library.db` (database)
- ❌ `static/uploads/` (ảnh upload)
- ❌ `.venv/` (virtual environment)
- ❌ `__pycache__/` (Python cache)
- ❌ `.env` (environment variables)

Các file sau sẽ **ĐƯỢC** push:
- ✅ Source code (`.py`)
- ✅ Templates (`.html`)
- ✅ `requirements.txt`
- ✅ `Dockerfile`, `docker-compose.yml`
- ✅ `README.md`
- ✅ Các file cấu hình khác

---

## 🎯 Tóm tắt nhanh

```powershell
# 1. Thay đổi remote
git remote set-url origin https://github.com/USERNAME/REPO.git

# 2. Commit (nếu cần)
git add .
git commit -m "Mô tả commit"

# 3. Push
git push -u origin main
```

**Xong!** 🎉

