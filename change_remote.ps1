# Script PowerShell để thay đổi remote GitHub
# Sử dụng: .\change_remote.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "THAY ĐỔI GITHUB REMOTE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Hiển thị remote hiện tại
Write-Host "Remote hiện tại:" -ForegroundColor Yellow
git remote -v
Write-Host ""

# Nhập thông tin repository mới
$username = Read-Host "Nhập GitHub username của bạn"
$repoName = Read-Host "Nhập tên repository mới"

# Tạo URL mới
$newUrl = "https://github.com/$username/$repoName.git"

Write-Host ""
Write-Host "Bạn muốn:" -ForegroundColor Yellow
Write-Host "1. Thay đổi remote hiện tại (origin)"
Write-Host "2. Thêm remote mới (không xóa remote cũ)"
$choice = Read-Host "Chọn (1 hoặc 2)"

if ($choice -eq "1") {
    Write-Host ""
    Write-Host "Đang thay đổi remote..." -ForegroundColor Green
    git remote set-url origin $newUrl
    Write-Host "✅ Đã thay đổi remote thành công!" -ForegroundColor Green
} elseif ($choice -eq "2") {
    $remoteName = Read-Host "Nhập tên remote mới (ví dụ: new-origin)"
    Write-Host ""
    Write-Host "Đang thêm remote mới..." -ForegroundColor Green
    git remote add $remoteName $newUrl
    Write-Host "✅ Đã thêm remote mới: $remoteName" -ForegroundColor Green
} else {
    Write-Host "❌ Lựa chọn không hợp lệ!" -ForegroundColor Red
    exit
}

Write-Host ""
Write-Host "Remote sau khi thay đổi:" -ForegroundColor Yellow
git remote -v
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Bước tiếp theo:" -ForegroundColor Cyan
Write-Host "1. git add ." -ForegroundColor White
Write-Host "2. git commit -m 'Mô tả commit'" -ForegroundColor White
Write-Host "3. git push -u origin main" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan

