from flask import Blueprint, render_template, jsonify, redirect, url_for
from flask_login import login_required, current_user
from datetime import date, timedelta, datetime
from sqlalchemy import func, desc
from ..models import Book, BorrowRecord, User, Reservation
from ..extensions import db
from functools import wraps

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


@dashboard_bp.route('/')
@login_required
def index():
    """Dashboard chính"""
    if current_user.is_admin:
        return admin_dashboard()
    else:
        return user_dashboard()


def admin_dashboard():
    """Dashboard cho admin"""
    # Thống kê tổng quan
    total_books = Book.query.count()
    total_users = User.query.count()
    total_borrows = BorrowRecord.query.filter(BorrowRecord.returned_at.is_(None)).count()
    overdue_books = BorrowRecord.query.filter(
        BorrowRecord.returned_at.is_(None),
        BorrowRecord.due_date < date.today()
    ).count()
    
    # Sách mượn nhiều nhất
    popular_books = db.session.query(
        Book,
        func.count(BorrowRecord.id).label('borrow_count')
    ).join(BorrowRecord).group_by(Book.id).order_by(desc('borrow_count')).limit(10).all()
    
    # Độc giả tích cực
    active_readers = db.session.query(
        User,
        func.count(BorrowRecord.id).label('borrow_count')
    ).join(BorrowRecord).group_by(User.id).order_by(desc('borrow_count')).limit(10).all()
    
    # Sách quá hạn
    overdue_records = BorrowRecord.query.filter(
        BorrowRecord.returned_at.is_(None),
        BorrowRecord.due_date < date.today()
    ).order_by(BorrowRecord.due_date).limit(20).all()
    
    # Đặt trước chưa thực hiện
    pending_reservations = Reservation.query.filter_by(fulfilled=False).count()
    
    # Thống kê theo tháng (7 tháng gần nhất)
    months_stats = []
    for i in range(6, -1, -1):
        month_start = date.today().replace(day=1) - timedelta(days=30*i)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        borrows_count = BorrowRecord.query.filter(
            BorrowRecord.borrowed_at >= datetime.combine(month_start, datetime.min.time()),
            BorrowRecord.borrowed_at <= datetime.combine(month_end, datetime.max.time())
        ).count()
        
        months_stats.append({
            'month': month_start.strftime('%m/%Y'),
            'count': borrows_count
        })
    
    return render_template('dashboard/admin_dashboard.html',
                         total_books=total_books,
                         total_users=total_users,
                         total_borrows=total_borrows,
                         overdue_books=overdue_books,
                         popular_books=popular_books,
                         active_readers=active_readers,
                         overdue_records=overdue_records,
                         pending_reservations=pending_reservations,
                         months_stats=months_stats,
                         today=date.today())


def user_dashboard():
    """Dashboard cho user"""
    # Sách đang mượn
    active_borrows = BorrowRecord.query.filter_by(
        user_id=current_user.id,
        returned_at=None
    ).order_by(BorrowRecord.due_date).all()
    
    # Sách quá hạn của user
    overdue_borrows = [b for b in active_borrows if b.is_overdue()]
    
    # Đặt trước của user
    my_reservations = Reservation.query.filter_by(
        user_id=current_user.id,
        fulfilled=False
    ).count()
    
    # Lịch sử mượn gần đây
    recent_borrows = BorrowRecord.query.filter_by(
        user_id=current_user.id
    ).order_by(BorrowRecord.borrowed_at.desc()).limit(10).all()
    
    return render_template('dashboard/user_dashboard.html',
                         active_borrows=active_borrows,
                         overdue_borrows=overdue_borrows,
                         my_reservations=my_reservations,
                         recent_borrows=recent_borrows,
                         today=date.today())


@dashboard_bp.route('/api/stats')
@login_required
def api_stats():
    """API trả về thống kê dạng JSON"""
    if not current_user.is_admin:
        return jsonify({'error': 'Không có quyền'}), 403
    
    stats = {
        'total_books': Book.query.count(),
        'total_users': User.query.count(),
        'active_borrows': BorrowRecord.query.filter(BorrowRecord.returned_at.is_(None)).count(),
        'overdue_books': BorrowRecord.query.filter(
            BorrowRecord.returned_at.is_(None),
            BorrowRecord.due_date < date.today()
        ).count()
    }
    
    return jsonify(stats)

