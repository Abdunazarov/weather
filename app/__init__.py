from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Конфигурация приложения
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Инициализация расширения Flask-Migrate для управления миграциями базы данных
migrate = Migrate(app, db)

def create_app(config_filename=None):
    """
    Фабрика приложений. Создает и настраивает экземпляр Flask приложения.
    """
    if config_filename:
        app.config.from_pyfile(config_filename)
    
    return app
