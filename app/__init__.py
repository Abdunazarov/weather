from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Инициализация расширения Flask-Migrate для управления миграциями базы данных
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # Конфигурация приложения
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../instance/sqlite.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from . import routes

    app.register_blueprint(routes.bp)

    return app
