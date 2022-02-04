from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config
from celery import Celery


app = Flask(__name__)
app.config.from_mapping(SQLALCHEMY_DATABASE_URI=config.POSTGRES_URL)
db = SQLAlchemy(app)

celery = Celery(
    __name__,
    backend='redis://localhost:6379/0',
    broker='redis://localhost:6379/1'
)
celery.conf.update(app.config)


class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)


celery.Task = ContextTask



