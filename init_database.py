"""
Script tự động khởi tạo database
Chạy: python init_database.py
"""
import os
import sys
from pathlib import Path

def init_database():
    """Khởi tạo database và tạo các bảng"""
    print("=" * 50)
    print("KHỞI TẠO DATABASE")
    print("=" * 50)
    
    # Thiết lập biến môi trường
    os.environ['FLASK_APP'] = 'src.app:create_app'
    
    try:
        from src.app import create_app
        from src.extensions import db
        from src.models import User, Book, BorrowRecord, Reservation
        
        app = create_app()
        
        with app.app_context():
            print("\n1. Đang tạo các bảng trong database...")
            
            # Tạo tất cả các bảng
            db.create_all()
            
            print("✅ Đã tạo các bảng thành công!")
            print("\nCác bảng đã được tạo:")
            print("  - users")
            print("  - books")
            print("  - borrow_records")
            print("  - reservations")
            
            # Kiểm tra xem đã có admin chưa
            admin_count = User.query.filter_by(is_admin=True).count()
            if admin_count == 0:
                print("\n⚠️  Chưa có tài khoản admin!")
                print("   Chạy: python create_admin.py để tạo admin")
            else:
                print(f"\n✅ Đã có {admin_count} tài khoản admin")
            
            print("\n" + "=" * 50)
            print("KHỞI TẠO HOÀN TẤT!")
            print("=" * 50)
            print("\nBây giờ bạn có thể:")
            print("  1. Chạy: python run.py")
            print("  2. Truy cập: http://localhost:5000")
            print("\nNếu chưa có admin, chạy: python create_admin.py")
            
    except Exception as e:
        print(f"\n❌ LỖI: {str(e)}")
        print("\nHướng dẫn khắc phục:")
        print("1. Đảm bảo đã kích hoạt virtual environment:")
        print("   .\\.venv\\Scripts\\Activate.ps1")
        print("\n2. Đảm bảo đã cài đặt dependencies:")
        print("   pip install -r requirements.txt")
        print("\n3. Thử chạy migrations thủ công:")
        print("   flask db init")
        print("   flask db migrate -m \"Initial migration\"")
        print("   flask db upgrade")
        sys.exit(1)

if __name__ == '__main__':
    init_database()

