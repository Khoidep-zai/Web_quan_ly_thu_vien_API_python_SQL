"""
Script để tạo tài khoản admin
Sử dụng: python create_admin.py
"""
from src.app import create_app
from src.models import User, db

app = create_app()

with app.app_context():
    email = input("Nhập email admin: ")
    name = input("Nhập tên admin: ")
    password = input("Nhập mật khẩu: ")
    
    # Kiểm tra xem email đã tồn tại chưa
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        print(f"Email {email} đã tồn tại. Cập nhật thành admin...")
        existing_user.is_admin = True
        if password:
            existing_user.set_password(password)
        db.session.commit()
        print("Đã cập nhật thành admin!")
    else:
        admin = User(email=email, name=name, is_admin=True)
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        print("Đã tạo tài khoản admin thành công!")

