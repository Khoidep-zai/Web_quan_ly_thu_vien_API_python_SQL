from flask import Flask, render_template
import os
from .config import Config
from .extensions import db, migrate, login_manager, mail, scheduler


def create_app():
    # Xác định đường dẫn static folder (ở thư mục gốc, không phải trong src/)
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    static_folder = os.path.join(basedir, 'static')
    template_folder = os.path.join(os.path.dirname(__file__), 'templates')
    
    app = Flask(__name__, 
                template_folder=template_folder, 
                static_folder=static_folder,
                static_url_path='/static')
    app.config.from_object(Config)

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    scheduler.init_app(app)
    
    # Chỉ start scheduler nếu chưa chạy (tránh lỗi khi reload)
    if not scheduler.running:
        scheduler.start()
        
        # Thiết lập scheduler jobs
        from .tasks.email_reminders import send_due_reminders, send_overdue_notifications
        
        # Gửi email nhắc nhở hàng ngày lúc 9:00 AM
        try:
            scheduler.add_job(
                id='send_due_reminders',
                func=send_due_reminders,
                trigger='cron',
                hour=9,
                minute=0,
                replace_existing=True
            )
        except Exception:
            pass  # Job đã tồn tại
        
        # Gửi email cảnh báo quá hạn hàng ngày lúc 9:30 AM
        try:
            scheduler.add_job(
                id='send_overdue_notifications',
                func=send_overdue_notifications,
                trigger='cron',
                hour=9,
                minute=30,
                replace_existing=True
            )
        except Exception:
            pass  # Job đã tồn tại

    # register blueprints
    from .routes.auth import auth_bp
    from .routes.books import books_bp
    from .routes.loans import loans_bp
    from .routes.reservations import reservations_bp
    from .routes.dashboard import dashboard_bp
    from .routes.reports import reports_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(loans_bp)
    app.register_blueprint(reservations_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(reports_bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app
