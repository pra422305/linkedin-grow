from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)
    app.instance_path and __import__("os").makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"

    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.profile import profile_bp
    from app.routes.content import content_bp
    from app.routes.networking import networking_bp
    from app.routes.analytics import analytics_bp
    from app.routes.agent import agent_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(content_bp)
    app.register_blueprint(networking_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(agent_bp)

    @app.cli.command("init-db")
    def init_db_command():
        db.create_all()
        _ensure_lightweight_columns()
        print("Database tables created.")

    return app


def _ensure_lightweight_columns():
    """Small SQLite-friendly upgrade path for classroom/demo databases."""
    from sqlalchemy import inspect, text

    inspector = inspect(db.engine)
    if "user_profile" not in inspector.get_table_names():
        return
    columns = {column["name"] for column in inspector.get_columns("user_profile")}
    if "linkedin_profile_url" not in columns:
        db.session.execute(text("ALTER TABLE user_profile ADD COLUMN linkedin_profile_url VARCHAR(500) DEFAULT ''"))

    if "analytics_record" in inspector.get_table_names():
        analytics_columns = {column["name"] for column in inspector.get_columns("analytics_record")}
        additions = {
            "profile_views": "INTEGER",
            "new_connections": "INTEGER",
            "linkedin_post_url": "VARCHAR(500) DEFAULT ''",
            "source": "VARCHAR(40) DEFAULT 'manual'",
        }
        for column, definition in additions.items():
            if column not in analytics_columns:
                db.session.execute(text(f"ALTER TABLE analytics_record ADD COLUMN {column} {definition}"))
    db.session.commit()
