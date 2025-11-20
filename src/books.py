from flask import Blueprint, request, jsonify, render_template, current_app
from .models import Book
from .extensions import db

books_bp = Blueprint('books', __name__, template_folder='templates')


@books_bp.route('/')
def list_books():
    q = request.args.get('q', '')
    query = Book.query
    if q:
        ilike = f"%{q}%"
        query = query.filter((Book.title.ilike(ilike)) | (Book.author.ilike(ilike)) | (Book.category.ilike(ilike)))
    page = int(request.args.get('page', 1))
    per_page = current_app.config.get('PER_PAGE', 20)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    books = pagination.items
    return render_template('books_list.html', books=books, pagination=pagination, q=q)


# Basic REST endpoint examples
@books_bp.route('/api', methods=['GET'])
def api_list_books():
    q = request.args.get('q', '')
    query = Book.query
    if q:
        ilike = f"%{q}%"
        query = query.filter((Book.title.ilike(ilike)) | (Book.author.ilike(ilike)) | (Book.category.ilike(ilike)))
    results = [
        {'id': b.id, 'title': b.title, 'author': b.author, 'available_copies': b.available_copies}
        for b in query.limit(100).all()
    ]
    return jsonify(results)
