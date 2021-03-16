
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)


class User(db.Model):

    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    @classmethod
    def register(cls, username, pwd, email, first, last):

        hashed = bcrypt.generate_password_hash(pwd).decode('utf8')
        return cls(username=username, password=hashed, email=email, first_name=first, last_name=last)

    @classmethod
    def authenticate(cls, username, pwd):
        user = cls.query.get(username=username)
        if user and bcrypt.check_password_hash(user.password, pwd):
            return user
        else:
            return False
