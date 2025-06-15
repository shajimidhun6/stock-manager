from app import db, create_app  # Adjust if your app init is elsewhere

app = create_app()  # Or whatever function or method you use to initialize your app

with app.app_context():
    db.create_all()
    print("Database created successfully.")
