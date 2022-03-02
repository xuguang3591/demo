from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

db = SQLAlchemy()
migrate = Migrate()


def init_ext(app):
    db.init_app(app)
    migrate.init_app(app, db)
    Session(app)