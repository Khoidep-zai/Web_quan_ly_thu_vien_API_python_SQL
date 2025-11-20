# Cấu trúc file — Hệ thống quản lý thư viện (Flask)

Tập tin này mô tả cây thư mục hiện tại, chức năng mỗi file/folder, và các liên kết (ai import/ai dùng ai). Mục đích: giúp người phát triển mới nhanh chóng hiểu codebase và biết chỉnh sửa ở đâu.

## Cây thư mục (hiện tại - rút gọn)

```
ĐỒ ÁN/
├─ Ảnh/
├─ docs/
│  └─ structure.md           # (this file)
├─ src/
│  ├─ app.py                 # create_app factory, đăng ký blueprints, khởi tạo scheduler
│  ├─ config.py              # cấu hình: DATABASE_URL, MAIL, các hằng số
│  ├─ extensions.py          # khởi tạo các extension (db, migrate, login, mail, scheduler)
│  ├─ models.py              # SQLAlchemy models: User, Book, BorrowRecord, Reservation
│  ├─ auth.py                # blueprint auth (login/register/logout)
│  ├─ books.py               # blueprint books (list, api endpoint)
│  └─ templates/
│     ├─ base.html
│     ├─ index.html
│     ├─ login.html
│     └─ register.html
├─ requirements.txt
├─ README.md
└─ .env.example
```

> Ghi chú: Khi phát triển, sẽ có thêm thư mục `migrations/` (Flask-Migrate) và có thể `static/`, `templates/admin/`, `tests/` v.v.

---

## Giải thích chi tiết theo file

### `src/app.py`
- Mục đích: factory function `create_app()` khởi tạo Flask app, config, khởi tạo và gắn các extension, đăng ký blueprints.
- Import / liên kết:
  - `from .config import Config` để nạp cấu hình
  - `from .extensions import db, migrate, login_manager, mail, scheduler` để init
  - đăng ký blueprints `auth_bp`, `books_bp` (nếu tồn tại)
- Khi cần thay đổi flow khởi tạo (ex: thêm API blueprint, cấu hình logging, WSGI settings) hãy sửa file này.

### `src/config.py`
- Mục đích: chứa class `Config` với các biến cấu hình mặc định và đọc từ environment.
- Các giá trị quan trọng:
  - `SQLALCHEMY_DATABASE_URI` (từ `DATABASE_URL`)
  - Mail config: `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USERNAME`, `MAIL_PASSWORD`
  - `REMINDER_DAYS_BEFORE`, `BORROW_DAYS_DEFAULT`
- Liên kết: `app.py` gọi `app.config.from_object(Config)`; các module khác có thể đọc `current_app.config['KEY']`.
- Sửa chỗ này cho cấu hình môi trường (dev/staging/prod).

### `src/extensions.py`
- Mục đích: khởi tạo các Flask extensions naked (không bind), để init trong `create_app()`.
- Exports: `db`, `migrate`, `login_manager`, `mail`, `scheduler`.
- Liên kết: `models.py` imports `db`; `app.py` gọi `db.init_app(app)`; các blueprints có thể import `login_manager`, `mail`, `scheduler`.

### `src/models.py`
- Mục đích: định nghĩa schema DB bằng SQLAlchemy ORM.
- Models chính:
  - `User`: thông tin độc giả, thuộc tính `is_admin`, mối quan hệ `borrow_records`, `reservations`.
  - `Book`: thông tin sách, `total_copies`, `available_copies`.
  - `BorrowRecord`: ghi nhận mượn/trả, `due_date`, `returned_at`, `fine_amount`.
  - `Reservation`: đặt trước sách.
- Liên kết:
  - Import `db` từ `extensions.py` (=> cần `extensions.py` tồn tại trước khi import)
  - Blueprint routes (ví dụ `auth.py`, `books.py`) đọc/ghi bảng này
- Khi thay đổi model, chạy `flask db migrate` và `flask db upgrade`.

### `src/auth.py`
- Mục đích: xử lý đăng nhập/đăng ký/đăng xuất (blueprint `auth_bp`). Template kèm theo: `login.html`, `register.html`.
- Liên kết:
  - Dùng `User` model từ `models.py` và `db` từ `extensions.py`.
  - `login_user`, `logout_user` từ `flask_login` (đã khởi tạo trong `extensions.py`).
- Thay đổi auth logic (ví dụ: thêm role-based access, đăng ký admin) ở đây.

### `src/books.py`
- Mục đích: hiển thị danh sách sách, API đơn giản (GET /books/api), xử lý tìm kiếm.
- Liên kết:
  - Dùng `Book` model và `db`.
  - Render template `books_list.html` (hiện chưa có — có thể thêm vào `templates/`).
- Nơi mở rộng: thêm CRUD, upload, CSV import, endpoints RESTful phiên bản đầy đủ.

### `src/templates/*.html`
- `base.html`: layout chính, import Bootstrap, nav bar, flash messages.
- `index.html`: trang chủ với form tìm kiếm
- `login.html`, `register.html`: form auth
- Liên kết: templates dùng `url_for()` để gọi endpoints trong `app.py`/blueprints.

### `requirements.txt`
- Liệt kê package cần cài. Khi thêm thư viện mới (ví dụ Celery, WeasyPrint), cập nhật file này.

### `.env.example`
- Mẫu biến môi trường: copy thành `.env` hoặc set biến môi trường trực tiếp.
- Chứa ví dụ `DATABASE_URL`, `MAIL_*`, `SECRET_KEY`, `REMINDER_DAYS_BEFORE`.

### `README.md`
- Hướng dẫn sử dụng, thiết lập và bảo trì (bạn đã cập nhật).

---

## Luồng import chính / dependency graph (đơn giản)

- `flask` app boot -> `src/app.py` (entry)
  - app.py -> imports `Config`, `extensions` -> calls `db.init_app`, `migrate.init_app`, `login_manager.init_app`, `mail.init_app`, `scheduler.init_app`
  - app.py -> registers blueprints (`auth`, `books`, ...)
- Blueprints (`auth.py`, `books.py`) -> import `models` and `db` để đọc/ghi dữ liệu
- `models.py` -> imports `db` từ `extensions.py`
- Templates -> gọi endpoints của blueprints
- Scheduler tasks (khi thêm) -> sẽ import `BorrowRecord`, `mail`, and use `current_app` for config

Đồ thị quan hệ (text):

app.py
  ├─ config.py
  ├─ extensions.py
  │   └─ db
  ├─ auth.py <─ models.py
  └─ books.py <─ models.py

Scheduler tasks -> models.py + extensions.mail

---

## Chỉ dẫn: muốn sửa gì thì chỉnh file nào

- Thêm model / trường mới -> chỉnh `src/models.py` → `flask db migrate` → `flask db upgrade`.
- Thêm route/endpoint mới -> tạo blueprint mới hoặc sửa `src/books.py`/`src/auth.py`.
- Thêm UI pages -> thêm template trong `src/templates/` và static assets trong `src/static/`.
- Thêm tính năng nền (email reminders) -> tạo module `src/tasks.py`, nhập `scheduler` từ `extensions.py`, đăng ký job trong `create_app()` hoặc `scheduler.init_app` config.
- Thêm cấu hình mới -> `src/config.py` và đọc giá trị từ biến môi trường.

---

## Gợi ý tổ chức mở rộng (khi dự án lớn hơn)
- Tách `blueprints/` thành thư mục `src/blueprints/{auth,books,admin}` each with `routes.py`, `forms.py`, `templates/`.
- Thêm `services/` hoặc `jobs/` để chứa logic nghiệp vụ (email, fines, reports) tránh lặp code trong routes.
- Thêm `tests/` với `conftest.py` để bootstrap test app và fixture DB.

---

## Liên hệ nhanh cho developer mới
- Để chạy dev: xem `README.md` (đã có hướng dẫn)
- Muốn tôi tự động tạo `docs/structure.md` (đã tạo) tiếp theo tôi có thể:
  - tạo `docs/api.md` (OpenAPI/REST spec sơ bộ)
  - tạo `src/tasks.py` + job mẫu gửi email



---

(End of `docs/structure.md`)
