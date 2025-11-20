from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
from ..models import Reservation, Book, BorrowRecord
from ..extensions import db
from functools import wraps

reservations_bp = Blueprint('reservations', __name__, url_prefix='/reservations')


def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Bạn không có quyền truy cập.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


@reservations_bp.route('/reserve/<int:book_id>', methods=['POST'])
@login_required
def reserve_book(book_id):
    """Đặt trước sách"""
    book = Book.query.get_or_404(book_id)
    
    # Kiểm tra xem sách có đang được mượn không
    if book.available_copies > 0:
        flash('Sách hiện có sẵn, bạn có thể mượn trực tiếp.', 'info')
        return redirect(url_for('books.list_books'))
    
    # Kiểm tra xem user đã đặt trước chưa
    existing_reservation = Reservation.query.filter_by(
        user_id=current_user.id,
        book_id=book_id,
        fulfilled=False
    ).first()
    
    if existing_reservation:
        flash('Bạn đã đặt trước sách này rồi.', 'warning')
        return redirect(url_for('books.list_books'))
    
    # Kiểm tra xem user đã mượn sách này chưa
    existing_borrow = BorrowRecord.query.filter_by(
        user_id=current_user.id,
        book_id=book_id,
        returned_at=None
    ).first()
    
    if existing_borrow:
        flash('Bạn đang mượn sách này rồi.', 'warning')
        return redirect(url_for('books.list_books'))
    
    # Tạo reservation
    reservation = Reservation(
        user_id=current_user.id,
        book_id=book_id,
        fulfilled=False
    )
    
    db.session.add(reservation)
    db.session.commit()
    
    flash(f'Đã đặt trước sách "{book.title}". Bạn sẽ được thông báo khi sách có sẵn.', 'success')
    return redirect(url_for('reservations.my_reservations'))


@reservations_bp.route('/my-reservations')
@login_required
def my_reservations():
    """Danh sách đặt trước của user"""
    reservations = Reservation.query.filter_by(
        user_id=current_user.id,
        fulfilled=False
    ).order_by(Reservation.reserved_at.desc()).all()
    return render_template('reservations/my_reservations.html', reservations=reservations)


@reservations_bp.route('/cancel/<int:reservation_id>', methods=['POST'])
@login_required
def cancel_reservation(reservation_id):
    """Hủy đặt trước"""
    reservation = Reservation.query.get_or_404(reservation_id)
    
    if reservation.user_id != current_user.id:
        flash('Bạn không có quyền hủy đặt trước này.', 'danger')
        return redirect(url_for('reservations.my_reservations'))
    
    db.session.delete(reservation)
    db.session.commit()
    
    flash('Đã hủy đặt trước.', 'success')
    return redirect(url_for('reservations.my_reservations'))


@reservations_bp.route('/all')
@admin_required
def all_reservations():
    """Danh sách tất cả đặt trước (chỉ admin)"""
    fulfilled = request.args.get('fulfilled', 'false')
    query = Reservation.query
    
    if fulfilled == 'true':
        query = query.filter_by(fulfilled=True)
    else:
        query = query.filter_by(fulfilled=False)
    
    reservations = query.order_by(Reservation.reserved_at.desc()).all()
    return render_template('reservations/all_reservations.html', reservations=reservations)


# RESTful API
@reservations_bp.route('/api/reserve/<int:book_id>', methods=['POST'])
@login_required
def api_reserve_book(book_id):
    """API đặt trước sách"""
    book = Book.query.get_or_404(book_id)
    
    if book.available_copies > 0:
        return jsonify({'error': 'Sách có sẵn, không cần đặt trước'}), 400
    
    existing_reservation = Reservation.query.filter_by(
        user_id=current_user.id,
        book_id=book_id,
        fulfilled=False
    ).first()
    
    if existing_reservation:
        return jsonify({'error': 'Đã đặt trước sách này rồi'}), 400
    
    reservation = Reservation(
        user_id=current_user.id,
        book_id=book_id,
        fulfilled=False
    )
    
    db.session.add(reservation)
    db.session.commit()
    
    return jsonify({
        'message': 'Đặt trước thành công',
        'reservation_id': reservation.id
    }), 201

