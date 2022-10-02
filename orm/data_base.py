from flask_sqlalchemy import SQLAlchemy
from decouple import config
from flask import Flask

db = SQLAlchemy()


def init_app(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATA_BASE_URL')
    db.init_app(app)
