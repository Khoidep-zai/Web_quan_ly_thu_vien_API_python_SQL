from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .extensions import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(120))
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    borrow_records = db.relationship('BorrowRecord', backref='user', lazy=True)
    reservations = db.relationship('Reservation', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.email}>"


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255))
    category = db.Column(db.String(120))
    isbn = db.Column(db.String(50), unique=True, index=True)
    total_copies = db.Column(db.Integer, default=1)
    available_copies = db.Column(db.Integer, default=1)
    image_path = db.Column(db.String(500), nullable=True)  # Đường dẫn hình ảnh
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    borrow_records = db.relationship('BorrowRecord', backref='book', lazy=True)
    reservations = db.relationship('Reservation', backref='book', lazy=True)

    def __repr__(self):
        return f"<Book {self.title} by {self.author}>"


class BorrowRecord(db.Model):
    __tablename__ = 'borrow_records'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    borrowed_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.Date, nullable=False)
    returned_at = db.Column(db.DateTime, nullable=True)
    fine_amount = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(50), default='borrowed')  # borrowed, returned, overdue

    def is_overdue(self):
        if self.returned_at:
            return False
        return date.today() > self.due_date

    def calculate_fine(self, per_day_rate=None):
        if not self.is_overdue():
            return 0.0
        if per_day_rate is None:
            from flask import current_app
            per_day_rate = current_app.config.get('FINE_PER_DAY', 0.5)
        days = (date.today() - self.due_date).days
        return days * per_day_rate

    def __repr__(self):
        return f"<BorrowRecord user={self.user_id} book={self.book_id} due={self.due_date}>"


class Reservation(db.Model):
    __tablename__ = 'reservations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    reserved_at = db.Column(db.DateTime, default=datetime.utcnow)
    fulfilled = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Reservation user={self.user_id} book={self.book_id}>"


# login user loader for flask-login
try:
    from .extensions import login_manager

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return db.session.get(User, int(user_id))
        except Exception:
            return None
except Exception:
    # extensions or login manager may not be available in some contexts (tests/development)
    pass
