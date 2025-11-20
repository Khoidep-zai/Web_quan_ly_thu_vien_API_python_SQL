"""
Script để thêm cột image_path vào bảng books
Chạy: python update_database_image.py
"""
import os
import sqlite3
from pathlib import Path

def update_database():
    """Thêm cột image_path vào bảng books nếu chưa có"""
    print("=" * 50)
    print("CẬP NHẬT DATABASE - THÊM CỘT HÌNH ẢNH")
    print("=" * 50)
    
    # Tìm file database
    db_path = Path("library.db")
    if not db_path.exists():
        print("❌ Không tìm thấy file library.db")
        print("   Chạy: python init_database.py trước")
        return
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Kiểm tra xem cột image_path đã tồn tại chưa
        cursor.execute("PRAGMA table_info(books)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'image_path' in columns:
            print("✅ Cột image_path đã tồn tại trong bảng books")
        else:
            print("📝 Đang thêm cột image_path vào bảng books...")
            cursor.execute("ALTER TABLE books ADD COLUMN image_path VARCHAR(500)")
            conn.commit()
            print("✅ Đã thêm cột image_path thành công!")
        
        # Tạo thư mục uploads nếu chưa có
        upload_dir = Path("static/uploads/books")
        upload_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ Đã tạo thư mục: {upload_dir}")
        
        conn.close()
        
        print("\n" + "=" * 50)
        print("HOÀN TẤT!")
        print("=" * 50)
        print("\nBây giờ bạn có thể:")
        print("  1. Thêm sách với hình ảnh")
        print("  2. Sửa sách để thêm/cập nhật hình ảnh")
        
    except Exception as e:
        print(f"\n❌ LỖI: {str(e)}")
        print("\nHướng dẫn khắc phục:")
        print("1. Đảm bảo file library.db tồn tại")
        print("2. Đảm bảo không có ứng dụng nào đang sử dụng database")
        print("3. Thử chạy lại script")

if __name__ == '__main__':
    update_database()

