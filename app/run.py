from main import create_app, db

# اپلیکیشن را برای محیط پروداکشن (یا توسعه) ایجاد می‌کنیم
app = create_app()

# این دستور را برای ساخت خودکار جداول در اولین اجرا اضافه می‌کنیم
with app.app_context():
    db.create_all()

