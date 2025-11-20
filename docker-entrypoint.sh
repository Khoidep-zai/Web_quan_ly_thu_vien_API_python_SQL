#!/bin/bash
set -e

echo "🚀 Starting Library Management System..."

# Chờ database sẵn sàng
echo "⏳ Waiting for database..."
if [ -n "$DATABASE_URL" ]; then
  until python -c "import psycopg2; psycopg2.connect('${DATABASE_URL}')" 2>/dev/null; do
    echo "Database is unavailable - sleeping"
    sleep 1
  done
  echo "✅ Database is ready!"
fi

# Chạy migrations
echo "📦 Running database migrations..."
flask db upgrade || echo "⚠️  Migrations may have already been applied"

# Khởi tạo database nếu cần
echo "🔧 Initializing database..."
python init_database.py || echo "⚠️  Database may already be initialized"

# Chạy ứng dụng
echo "🌟 Starting application..."
exec "$@"

