from datetime import timedelta

from flask_sqlalchemy import SQLAlchemy
from decouple import config as conf
from flask import Flask
from celery import Celery

db = SQLAlchemy()


def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    task_base = celery.Task

    class ContextTask(task_base):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return task_base.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery


def init_app(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = conf('DATA_BASE_URL')
    app.config.update(
        CELERY_BROKER_URL=conf('CELERY_BROKER_URL'),
        CELERYBEAT_SCHEDULE={
            'test': {
                'task': 'task_ola_mundo',
                'schedule': timedelta(seconds=10)
            },
            'test_2': {
                'task': 'task_ola_mundo_2',
                'schedule': timedelta(seconds=20)
            },
        }
    )
    db.init_app(app)
    make_celery(app)
