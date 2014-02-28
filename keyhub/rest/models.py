from flask.ext.sqlalchemy import SQLAlchemy
from keyhub.wsgi import app
from keyhub.exceptions import KeyhubError


db = SQLAlchemy(app)


class BaseModel(object):
    @classmethod
    def get_by(cls, **kwargs):
        rows = cls.query.filter_by(**kwargs)
        if rows.count() == 1:
            return rows.first()
        elif rows.count() == 0:
            return None
        else:
            raise ValueError("More than 1 rows matched")

    def __getitem__(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        else:
            raise KeyError(key)

    @property
    def logger(self):
        if not hasattr(self, "_logger") or not self._logger:
            self._logger = logging.getLogger(self.__class__.__name__)

        return self._logger

    def save(self):
        db.session.add(self)
        db.session.commit()


class User(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


class SSHKey(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('keys', lazy='dynamic'))

    @classmethod
    def get_by_username(cls, username, key_id=None):
        user = User.query.filter_by(username=username)
        if user.count() >= 1:
            user = user.first()
        else:
            raise KeyhubError("User %s not found" % username)

        q = cls.query.filter_by(user_id=user.id)
        if key_id:
            q = q.filter_by(id=key_id)

        return q
