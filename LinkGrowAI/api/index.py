from app import create_app, db

app = create_app()

with app.app_context():
    try:
        db.create_all()
    except Exception as exc:
        app.logger.warning(f"Auto DB init warning: {exc}")
