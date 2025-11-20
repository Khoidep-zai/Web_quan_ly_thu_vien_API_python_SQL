from datetime import date, timedelta
from flask import current_app
from flask_mail import Message
from ..models import BorrowRecord
from ..extensions import db, mail


def send_due_reminders():
    """Gửi email nhắc nhở trả sách trước 3 ngày"""
    with current_app.app_context():
        reminder_days = current_app.config.get('REMINDER_DAYS_BEFORE', 3)
        target_date = date.today() + timedelta(days=reminder_days)
        
        # Tìm các bản ghi mượn sách có hạn trả = target_date và chưa trả
        records = BorrowRecord.query.filter(
            BorrowRecord.returned_at.is_(None),
            BorrowRecord.due_date == target_date
        ).all()
        
        sent_count = 0
        for record in records:
            try:
                user = record.user
                book = record.book
                
                # Tạo nội dung email
                subject = f'Nhắc nhở: Sách "{book.title}" sắp đến hạn trả'
                body = f"""
Xin chào {user.name or user.email},

Đây là email nhắc nhở từ hệ thống quản lý thư viện.

Bạn đã mượn sách "{book.title}" của tác giả {book.author or 'N/A'}.
Hạn trả sách: {record.due_date.strftime('%d/%m/%Y')}
Còn {reminder_days} ngày nữa là đến hạn trả.

Vui lòng trả sách đúng hạn để tránh phí trễ hạn.

Trân trọng,
Hệ thống quản lý thư viện
                """
                
                msg = Message(
                    subject=subject,
                    recipients=[user.email],
                    body=body
                )
                
                mail.send(msg)
                sent_count += 1
                
            except Exception as e:
                current_app.logger.error(f'Lỗi gửi email cho user {record.user_id}: {str(e)}')
                continue
        
        current_app.logger.info(f'Đã gửi {sent_count} email nhắc nhở')
        return sent_count


def send_overdue_notifications():
    """Gửi email thông báo sách quá hạn"""
    with current_app.app_context():
        today = date.today()
        
        # Tìm các bản ghi quá hạn
        records = BorrowRecord.query.filter(
            BorrowRecord.returned_at.is_(None),
            BorrowRecord.due_date < today
        ).all()
        
        sent_count = 0
        for record in records:
            try:
                user = record.user
                book = record.book
                days_overdue = (today - record.due_date).days
                fine = record.calculate_fine()
                
                subject = f'Cảnh báo: Sách "{book.title}" đã quá hạn trả'
                body = f"""
Xin chào {user.name or user.email},

Đây là email cảnh báo từ hệ thống quản lý thư viện.

Bạn đã mượn sách "{book.title}" của tác giả {book.author or 'N/A'}.
Hạn trả sách: {record.due_date.strftime('%d/%m/%Y')}
Sách đã quá hạn {days_overdue} ngày.

Phí trễ hạn hiện tại: {fine:.0f} VNĐ
Phí sẽ tiếp tục tăng mỗi ngày cho đến khi bạn trả sách.

Vui lòng trả sách sớm nhất có thể.

Trân trọng,
Hệ thống quản lý thư viện
                """
                
                msg = Message(
                    subject=subject,
                    recipients=[user.email],
                    body=body
                )
                
                mail.send(msg)
                sent_count += 1
                
            except Exception as e:
                current_app.logger.error(f'Lỗi gửi email cho user {record.user_id}: {str(e)}')
                continue
        
        current_app.logger.info(f'Đã gửi {sent_count} email cảnh báo quá hạn')
        return sent_count

