from flask import Blueprint, make_response, request
from flask_login import login_required, current_user
from datetime import date, datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from sqlalchemy import func, desc
from ..models import Book, BorrowRecord, User, Reservation
from ..extensions import db
from functools import wraps
import io

reports_bp = Blueprint('reports', __name__, url_prefix='/reports')


def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


@reports_bp.route('/borrows')
@admin_required
def borrows_report():
    """Xuất báo cáo mượn/trả PDF"""
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
    
    # Tạo PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=1  # Center
    )
    
    # Tiêu đề
    title = Paragraph("BÁO CÁO MƯỢN/TRẢ SÁCH", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    # Thông tin báo cáo
    info_text = f"Ngày xuất: {datetime.now().strftime('%d/%m/%Y %H:%M')}<br/>"
    info_text += f"Trạng thái: {status.upper()}<br/>"
    info_text += f"Tổng số: {len(borrows)} bản ghi"
    info_para = Paragraph(info_text, styles['Normal'])
    elements.append(info_para)
    elements.append(Spacer(1, 0.3*inch))
    
    # Bảng dữ liệu
    data = [['STT', 'Độc giả', 'Sách', 'Ngày mượn', 'Hạn trả', 'Ngày trả', 'Phí', 'Trạng thái']]
    
    for idx, borrow in enumerate(borrows, 1):
        status_text = 'Quá hạn' if borrow.is_overdue() and not borrow.returned_at else (
            'Đã trả' if borrow.returned_at else 'Đang mượn'
        )
        returned = borrow.returned_at.strftime('%d/%m/%Y') if borrow.returned_at else '-'
        
        row = [
            str(idx),
            borrow.user.name or borrow.user.email,
            borrow.book.title,
            borrow.borrowed_at.strftime('%d/%m/%Y'),
            borrow.due_date.strftime('%d/%m/%Y'),
            returned,
            f"{borrow.fine_amount:.0f}" if borrow.fine_amount > 0 else '-',
            status_text
        ]
        data.append(row)
    
    table = Table(data, colWidths=[0.4*inch, 1.2*inch, 1.5*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.6*inch, 0.8*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))
    
    elements.append(table)
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=bao_cao_muon_tra_{status}_{datetime.now().strftime("%Y%m%d")}.pdf'
    
    return response


@reports_bp.route('/books')
@admin_required
def books_report():
    """Xuất báo cáo sách PDF"""
    books = Book.query.order_by(Book.title).all()
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=1
    )
    
    title = Paragraph("BÁO CÁO DANH SÁCH SÁCH", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    info_text = f"Ngày xuất: {datetime.now().strftime('%d/%m/%Y %H:%M')}<br/>"
    info_text += f"Tổng số sách: {len(books)}"
    info_para = Paragraph(info_text, styles['Normal'])
    elements.append(info_para)
    elements.append(Spacer(1, 0.3*inch))
    
    data = [['STT', 'Tên sách', 'Tác giả', 'Thể loại', 'ISBN', 'Tổng số', 'Có sẵn']]
    
    for idx, book in enumerate(books, 1):
        row = [
            str(idx),
            book.title,
            book.author or '-',
            book.category or '-',
            book.isbn or '-',
            str(book.total_copies),
            str(book.available_copies)
        ]
        data.append(row)
    
    table = Table(data, colWidths=[0.4*inch, 2*inch, 1.2*inch, 1*inch, 1*inch, 0.6*inch, 0.6*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))
    
    elements.append(table)
    doc.build(elements)
    buffer.seek(0)
    
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=bao_cao_sach_{datetime.now().strftime("%Y%m%d")}.pdf'
    
    return response


@reports_bp.route('/statistics')
@admin_required
def statistics_report():
    """Xuất báo cáo thống kê PDF"""
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
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=1
    )
    
    title = Paragraph("BÁO CÁO THỐNG KÊ", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    info_text = f"Ngày xuất: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    info_para = Paragraph(info_text, styles['Normal'])
    elements.append(info_para)
    elements.append(Spacer(1, 0.3*inch))
    
    # Thống kê tổng quan
    summary_title = Paragraph("<b>THỐNG KÊ TỔNG QUAN</b>", styles['Heading2'])
    elements.append(summary_title)
    elements.append(Spacer(1, 0.1*inch))
    
    summary_data = [
        ['Chỉ số', 'Giá trị'],
        ['Tổng số sách', str(total_books)],
        ['Tổng số độc giả', str(total_users)],
        ['Sách đang mượn', str(total_borrows)],
        ['Sách quá hạn', str(overdue_books)]
    ]
    
    summary_table = Table(summary_data, colWidths=[2*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Sách mượn nhiều nhất
    popular_title = Paragraph("<b>TOP 10 SÁCH MƯỢN NHIỀU NHẤT</b>", styles['Heading2'])
    elements.append(popular_title)
    elements.append(Spacer(1, 0.1*inch))
    
    popular_data = [['STT', 'Tên sách', 'Tác giả', 'Số lần mượn']]
    for idx, (book, count) in enumerate(popular_books, 1):
        popular_data.append([str(idx), book.title, book.author or '-', str(count)])
    
    popular_table = Table(popular_data, colWidths=[0.5*inch, 2*inch, 1.5*inch, 1*inch])
    popular_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
    ]))
    elements.append(popular_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Độc giả tích cực
    readers_title = Paragraph("<b>TOP 10 ĐỘC GIẢ TÍCH CỰC</b>", styles['Heading2'])
    elements.append(readers_title)
    elements.append(Spacer(1, 0.1*inch))
    
    readers_data = [['STT', 'Tên độc giả', 'Email', 'Số lần mượn']]
    for idx, (user, count) in enumerate(active_readers, 1):
        readers_data.append([str(idx), user.name or '-', user.email, str(count)])
    
    readers_table = Table(readers_data, colWidths=[0.5*inch, 1.5*inch, 2*inch, 1*inch])
    readers_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
    ]))
    elements.append(readers_table)
    
    doc.build(elements)
    buffer.seek(0)
    
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=bao_cao_thong_ke_{datetime.now().strftime("%Y%m%d")}.pdf'
    
    return response

