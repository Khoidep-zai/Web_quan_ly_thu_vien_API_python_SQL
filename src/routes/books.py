from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from ..models import Book
from ..extensions import db
from functools import wraps
import os
from pathlib import Path

books_bp = Blueprint('books', __name__, url_prefix='/books')


def allowed_file(filename):
    """Kiểm tra file có phải là ảnh hợp lệ không"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config.get('ALLOWED_EXTENSIONS', {'png', 'jpg', 'jpeg', 'gif', 'webp'})


def save_book_image(file, book_id):
    """Lưu hình ảnh sách và trả về đường dẫn"""
    if file and allowed_file(file.filename):
        # Tạo thư mục nếu chưa có
        upload_folder = current_app.config.get('UPLOAD_FOLDER')
        Path(upload_folder).mkdir(parents=True, exist_ok=True)
        
        # Tạo tên file an toàn
        filename = secure_filename(file.filename)
        # Đổi tên thành book_id + extension để tránh trùng
        ext = filename.rsplit('.', 1)[1].lower()
        filename = f"book_{book_id}.{ext}"
        
        # Lưu file
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        # Trả về đường dẫn tương đối từ static
        return f"uploads/books/{filename}"
    return None


def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Bạn không có quyền truy cập.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


@books_bp.route('/')
def list_books():
    """Danh sách sách với tìm kiếm"""
    q = request.args.get('q', '')
    category = request.args.get('category', '')
    author = request.args.get('author', '')
    
    query = Book.query
    
    if q:
        ilike = f"%{q}%"
        query = query.filter(
            (Book.title.ilike(ilike)) | 
            (Book.author.ilike(ilike)) | 
            (Book.category.ilike(ilike)) |
            (Book.isbn.ilike(ilike))
        )
    
    if category:
        query = query.filter(Book.category.ilike(f"%{category}%"))
    
    if author:
        query = query.filter(Book.author.ilike(f"%{author}%"))
    
    page = int(request.args.get('page', 1))
    per_page = current_app.config.get('PER_PAGE', 20)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    books = pagination.items
    
    # Lấy danh sách thể loại và tác giả để filter
    categories = db.session.query(Book.category).distinct().filter(Book.category.isnot(None)).all()
    categories = [c[0] for c in categories if c[0]]
    
    authors = db.session.query(Book.author).distinct().filter(Book.author.isnot(None)).all()
    authors = [a[0] for a in authors if a[0]]
    
    return render_template('books/list.html', 
                         books=books, 
                         pagination=pagination, 
                         q=q,
                         category=category,
                         author=author,
                         categories=categories,
                         authors=authors)


@books_bp.route('/<int:book_id>')
def detail(book_id):
    """Chi tiết sách"""
    book = Book.query.get_or_404(book_id)
    return render_template('books/detail.html', book=book)


@books_bp.route('/add', methods=['GET', 'POST'])
@admin_required
def add():
    """Thêm sách mới (chỉ admin)"""
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        category = request.form.get('category')
        isbn = request.form.get('isbn')
        total_copies = int(request.form.get('total_copies', 1))
        
        if not title:
            flash('Tên sách là bắt buộc.', 'danger')
            return render_template('books/form.html')
        
        # Kiểm tra ISBN trùng
        if isbn and Book.query.filter_by(isbn=isbn).first():
            flash('ISBN đã tồn tại.', 'warning')
            return render_template('books/form.html')
        
        book = Book(
            title=title,
            author=author,
            category=category,
            isbn=isbn,
            total_copies=total_copies,
            available_copies=total_copies
        )
        
        db.session.add(book)
        db.session.flush()  # Lấy ID của book trước khi commit
        
        # Xử lý upload hình ảnh
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '':
                if allowed_file(file.filename):
                    image_path = save_book_image(file, book.id)
                    if image_path:
                        book.image_path = image_path
                else:
                    flash('Chỉ chấp nhận file ảnh (png, jpg, jpeg, gif, webp).', 'warning')
        
        db.session.commit()
        
        flash(f'Đã thêm sách "{title}" thành công.', 'success')
        return redirect(url_for('books.detail', book_id=book.id))
    
    return render_template('books/form.html')


@books_bp.route('/<int:book_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit(book_id):
    """Sửa thông tin sách (chỉ admin)"""
    book = Book.query.get_or_404(book_id)
    
    if request.method == 'POST':
        book.title = request.form.get('title')
        book.author = request.form.get('author')
        book.category = request.form.get('category')
        isbn = request.form.get('isbn')
        total_copies = int(request.form.get('total_copies', 1))
        
        # Kiểm tra ISBN trùng (trừ chính nó)
        if isbn and isbn != book.isbn:
            existing = Book.query.filter_by(isbn=isbn).first()
            if existing:
                flash('ISBN đã tồn tại.', 'warning')
                return render_template('books/form.html', book=book)
        
        book.isbn = isbn
        
        # Cập nhật số lượng
        old_total = book.total_copies
        book.total_copies = total_copies
        # Điều chỉnh available_copies
        diff = total_copies - old_total
        book.available_copies = max(0, book.available_copies + diff)
        
        # Xử lý upload hình ảnh mới
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '':
                if allowed_file(file.filename):
                    # Xóa ảnh cũ nếu có
                    if book.image_path:
                        old_image_path = os.path.join(current_app.static_folder, book.image_path)
                        if os.path.exists(old_image_path):
                            try:
                                os.remove(old_image_path)
                            except Exception:
                                pass
                    
                    # Lưu ảnh mới
                    image_path = save_book_image(file, book.id)
                    if image_path:
                        book.image_path = image_path
                else:
                    flash('Chỉ chấp nhận file ảnh (png, jpg, jpeg, gif, webp).', 'warning')
        
        db.session.commit()
        
        flash('Đã cập nhật thông tin sách.', 'success')
        return redirect(url_for('books.detail', book_id=book.id))
    
    return render_template('books/form.html', book=book)


@books_bp.route('/<int:book_id>/delete', methods=['POST'])
@admin_required
def delete(book_id):
    """Xóa sách (chỉ admin)"""
    book = Book.query.get_or_404(book_id)
    
    # Kiểm tra xem sách có đang được mượn không
    from ..models import BorrowRecord
    active_borrows = BorrowRecord.query.filter_by(
        book_id=book_id,
        returned_at=None
    ).count()
    
    if active_borrows > 0:
        flash(f'Không thể xóa sách. Có {active_borrows} bản đang được mượn.', 'danger')
        return redirect(url_for('books.detail', book_id=book_id))
    
    title = book.title
    db.session.delete(book)
    db.session.commit()
    
    flash(f'Đã xóa sách "{title}".', 'success')
    return redirect(url_for('books.list_books'))


# RESTful API endpoints
@books_bp.route('/api')
def api_list_books():
    """API danh sách sách"""
    q = request.args.get('q', '')
    category = request.args.get('category', '')
    author = request.args.get('author', '')
    limit = int(request.args.get('limit', 100))
    
    query = Book.query
    
    if q:
        ilike = f"%{q}%"
        query = query.filter(
            (Book.title.ilike(ilike)) | 
            (Book.author.ilike(ilike)) | 
            (Book.category.ilike(ilike))
        )
    
    if category:
        query = query.filter(Book.category.ilike(f"%{category}%"))
    
    if author:
        query = query.filter(Book.author.ilike(f"%{author}%"))
    
    books = query.limit(limit).all()
    
    results = [{
        'id': b.id,
        'title': b.title,
        'author': b.author,
        'category': b.category,
        'isbn': b.isbn,
        'total_copies': b.total_copies,
        'available_copies': b.available_copies
    } for b in books]
    
    return jsonify(results)


@books_bp.route('/api/<int:book_id>')
def api_book_detail(book_id):
    """API chi tiết sách"""
    book = Book.query.get_or_404(book_id)
    return jsonify({
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'category': book.category,
        'isbn': book.isbn,
        'total_copies': book.total_copies,
        'available_copies': book.available_copies,
        'created_at': book.created_at.isoformat() if book.created_at else None
    })


@books_bp.route('/api', methods=['POST'])
@admin_required
def api_create_book():
    """API tạo sách mới"""
    data = request.get_json()
    
    if not data or not data.get('title'):
        return jsonify({'error': 'Tên sách là bắt buộc'}), 400
    
    if data.get('isbn') and Book.query.filter_by(isbn=data['isbn']).first():
        return jsonify({'error': 'ISBN đã tồn tại'}), 400
    
    book = Book(
        title=data['title'],
        author=data.get('author'),
        category=data.get('category'),
        isbn=data.get('isbn'),
        total_copies=data.get('total_copies', 1),
        available_copies=data.get('total_copies', 1)
    )
    
    db.session.add(book)
    db.session.commit()
    
    return jsonify({
        'id': book.id,
        'title': book.title,
        'message': 'Tạo sách thành công'
    }), 201


@books_bp.route('/api/<int:book_id>', methods=['PUT'])
@admin_required
def api_update_book(book_id):
    """API cập nhật sách"""
    book = Book.query.get_or_404(book_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Không có dữ liệu'}), 400
    
    if 'title' in data:
        book.title = data['title']
    if 'author' in data:
        book.author = data['author']
    if 'category' in data:
        book.category = data['category']
    if 'isbn' in data:
        if data['isbn'] != book.isbn and Book.query.filter_by(isbn=data['isbn']).first():
            return jsonify({'error': 'ISBN đã tồn tại'}), 400
        book.isbn = data['isbn']
    if 'total_copies' in data:
        old_total = book.total_copies
        book.total_copies = data['total_copies']
        diff = data['total_copies'] - old_total
        book.available_copies = max(0, book.available_copies + diff)
    
    db.session.commit()
    
    return jsonify({
        'id': book.id,
        'title': book.title,
        'message': 'Cập nhật thành công'
    }), 200


@books_bp.route('/api/<int:book_id>', methods=['DELETE'])
@admin_required
def api_delete_book(book_id):
    """API xóa sách"""
    book = Book.query.get_or_404(book_id)
    
    from ..models import BorrowRecord
    active_borrows = BorrowRecord.query.filter_by(
        book_id=book_id,
        returned_at=None
    ).count()
    
    if active_borrows > 0:
        return jsonify({'error': f'Có {active_borrows} bản đang được mượn'}), 400
    
    db.session.delete(book)
    db.session.commit()
    
    return jsonify({'message': 'Xóa sách thành công'}), 200

