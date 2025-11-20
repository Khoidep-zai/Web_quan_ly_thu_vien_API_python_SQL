from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime, date, timedelta
from ..models import BorrowRecord, Book, User, Reservation
from ..extensions import db
from functools import wraps

loans_bp = Blueprint('loans', __name__, url_prefix='/loans')


def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Bạn không có quyền truy cập.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


@loans_bp.route('/borrow/<int:book_id>', methods=['POST'])
@login_required
def borrow_book(book_id):
    """Mượn sách"""
    book = Book.query.get_or_404(book_id)
    
    if book.available_copies <= 0:
        flash('Sách hiện không có sẵn.', 'warning')
        return redirect(url_for('books.list_books'))
    
    # Kiểm tra xem user đã mượn sách này chưa
    existing_borrow = BorrowRecord.query.filter_by(
        user_id=current_user.id,
        book_id=book_id,
        returned_at=None
    ).first()
    
    if existing_borrow:
        flash('Bạn đã mượn sách này rồi.', 'warning')
        return redirect(url_for('books.list_books'))
    
    # Tạo record mượn sách
    due_date = date.today() + timedelta(days=14)  # Mặc định 14 ngày
    borrow_record = BorrowRecord(
        user_id=current_user.id,
        book_id=book_id,
        due_date=due_date,
        status='borrowed'
    )
    
    book.available_copies -= 1
    db.session.add(borrow_record)
    db.session.commit()
    
    flash(f'Đã mượn sách "{book.title}". Hạn trả: {due_date.strftime("%d/%m/%Y")}', 'success')
    return redirect(url_for('loans.my_loans'))


@loans_bp.route('/return/<int:borrow_id>', methods=['POST'])
@login_required
def return_book(borrow_id):
    """Trả sách"""
    borrow_record = BorrowRecord.query.get_or_404(borrow_id)
    
    # Kiểm tra quyền: chỉ user mượn hoặc admin mới được trả
    if borrow_record.user_id != current_user.id and not current_user.is_admin:
        flash('Bạn không có quyền trả sách này.', 'danger')
        return redirect(url_for('loans.my_loans'))
    
    if borrow_record.returned_at:
        flash('Sách này đã được trả rồi.', 'warning')
        return redirect(url_for('loans.my_loans'))
    
    # Tính phạt nếu trễ hạn
    fine = borrow_record.calculate_fine()
    borrow_record.fine_amount = fine
    borrow_record.returned_at = datetime.utcnow()
    borrow_record.status = 'returned'
    
    # Tăng số lượng sách có sẵn
    book = borrow_record.book
    book.available_copies += 1
    
    # Kiểm tra và xử lý đặt trước
    reservation = Reservation.query.filter_by(
        book_id=book.id,
        fulfilled=False
    ).order_by(Reservation.reserved_at).first()
    
    if reservation:
        # Có thể tự động chuyển sách cho người đặt trước
        pass
    
    db.session.commit()
    
    if fine > 0:
        flash(f'Đã trả sách. Phí trễ hạn: {fine:.2f} VNĐ', 'warning')
    else:
        flash('Đã trả sách thành công.', 'success')
    
    return redirect(url_for('loans.my_loans'))


@loans_bp.route('/my-loans')
@login_required
def my_loans():
    """Danh sách sách đã mượn của user hiện tại"""
    borrows = BorrowRecord.query.filter_by(user_id=current_user.id).order_by(
        BorrowRecord.borrowed_at.desc()
    ).all()
    return render_template('loans/my_loans.html', borrows=borrows)


@loans_bp.route('/all')
@admin_required
def all_loans():
    """Danh sách tất cả mượn/trả (chỉ admin)"""
    status = request.args.get('status', 'all')
    query = BorrowRecord.query
    
    if status == 'active':
        query = query.filter(BorrowRecord.returned_at.is_(None))
    elif status == 'overdue':
        query = query.filter(
            BorrowRecord.returned_at.is_(None),
            BorrowRecord.due_date < date.today()
        )
    elif status == 'returned':
        query = query.filter(BorrowRecord.returned_at.isnot(None))
    
    borrows = query.order_by(BorrowRecord.borrowed_at.desc()).all()
    return render_template('loans/all_loans.html', borrows=borrows, status=status)


# RESTful API endpoints
@loans_bp.route('/api/borrow/<int:book_id>', methods=['POST'])
@login_required
def api_borrow_book(book_id):
    """API mượn sách"""
    book = Book.query.get_or_404(book_id)
    
    if book.available_copies <= 0:
        return jsonify({'error': 'Sách không có sẵn'}), 400
    
    existing_borrow = BorrowRecord.query.filter_by(
        user_id=current_user.id,
        book_id=book_id,
        returned_at=None
    ).first()
    
    if existing_borrow:
        return jsonify({'error': 'Bạn đã mượn sách này rồi'}), 400
    
    due_date = date.today() + timedelta(days=14)
    borrow_record = BorrowRecord(
        user_id=current_user.id,
        book_id=book_id,
        due_date=due_date,
        status='borrowed'
    )
    
    book.available_copies -= 1
    db.session.add(borrow_record)
    db.session.commit()
    
    return jsonify({
        'message': 'Mượn sách thành công',
        'borrow_id': borrow_record.id,
        'due_date': due_date.isoformat()
    }), 201


@loans_bp.route('/api/return/<int:borrow_id>', methods=['POST'])
@login_required
def api_return_book(borrow_id):
    """API trả sách"""
    borrow_record = BorrowRecord.query.get_or_404(borrow_id)
    
    if borrow_record.user_id != current_user.id and not current_user.is_admin:
        return jsonify({'error': 'Không có quyền'}), 403
    
    if borrow_record.returned_at:
        return jsonify({'error': 'Sách đã được trả'}), 400
    
    fine = borrow_record.calculate_fine()
    borrow_record.fine_amount = fine
    borrow_record.returned_at = datetime.utcnow()
    borrow_record.status = 'returned'
    
    book = borrow_record.book
    book.available_copies += 1
    db.session.commit()
    
    return jsonify({
        'message': 'Trả sách thành công',
        'fine': fine
    }), 200

