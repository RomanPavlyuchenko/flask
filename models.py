import hashlib
from secrets import token_hex, compare_digest
from datetime import datetime

from sqlalchemy import exc

import config
import errors
from app import db


class BaseModelMixin:

    @classmethod
    def get(cls, id):
        obj = cls.query.get(id)
        if obj:
            return obj
        else:
            raise errors.NotFound

    def add(self):
        db.session.add(self)
        try:
            db.session.commit()
        except exc.IntegrityError:
            raise errors.IntegrityError


class User(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    token = db.Column(db.String(128))
    advertisements = db.relationship('Advertisement', backref='owner')

    def __str__(self):
        return f'<User {self.username}>'

    def __repr__(self):
        return str(self)

    @classmethod
    def verify_user(cls, username, token):
        user = cls.query.filter_by(username=username).first()
        if user:
            return compare_digest(
                user.token,
                hashlib.md5(f'{token}{config.SALT}'.encode()).hexdigest()
            )
        else:
            raise errors.AuthError

    def set_token(self):
        token = token_hex(32)
        salted_token = f'{token}{config.SALT}'
        self.token = hashlib.md5(salted_token.encode()).hexdigest()
        return token

    def set_password(self, password):
        password = f'{password}{config.SALT}'
        self.password = hashlib.md5(password.encode()).hexdigest()

    def check_password(self, password):
        password = f'{password}{config.SALT}'
        return self.password == hashlib.md5(password.encode()).hexdigest()

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

    @classmethod
    def get_by_name(cls, username):
        return User.query.filter_by(username=username).first()



class Advertisement(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __str__(self):
        return f'<Adv {self.title}'

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'created': self.created,
            'owner': self.owner.id
        }

    def add(self):
        db.session.add(self)
        try:
            db.session.commit()
        except exc.IntegrityError:
            raise errors.IntegrityError

    def delete(self):
        db.session.delete(self)
        try:
            db.session.commit()
        except exc.IntegrityError:
            raise errors.IntegrityError
