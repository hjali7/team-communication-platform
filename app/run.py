import os
import sys
from main import create_app, db

# --- Debugging Step ---
# خواندن تمام متغیرهای محیطی مربوط به دیتابیس
db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("POSTGRES_DB")
db_host = os.getenv("DB_HOST")

# چاپ کردن مقادیری که اپلیکیشن "می‌بیند"
print("--- DATABASE CONNECTION DEBUG ---", file=sys.stderr)
print(f"DB_HOST: {db_host}", file=sys.stderr)
print(f"DB_USER: {db_user}", file=sys.stderr)
print(f"DB_NAME: {db_name}", file=sys.stderr)
print(f"DB_PASS is set: {'Yes' if db_password else 'No'}", file=sys.stderr)
print("---------------------------------", file=sys.stderr)
sys.stderr.flush()

# --- App Execution ---
app = create_app()

# ایجاد جداول دیتابیس با مدیریت خطا
with app.app_context():
    try:
        print("Attempting to create database tables...", file=sys.stderr)
        db.create_all()
        print("Database tables created successfully or already exist.", file=sys.stderr)
        sys.stderr.flush()
    except Exception as e:
        print(f"!!! DATABASE CONNECTION FAILED !!!", file=sys.stderr)
        print(f"Error: {e}", file=sys.stderr)
        sys.stderr.flush()
        # خروج با خطا برای اینکه کوبرنتیز متوجه مشکل شود
        sys.exit(1)

