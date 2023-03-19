import sqlalchemy as sa

from flask_login import LoginManager
from src.db import db


class User(db.Model):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_name = sa.Column(sa.String(30), unique=True, nullable=False)
    name = sa.Column(sa.String(80), nullable=False)
    email = sa.Column(sa.String(30), unique=True, nullable=False)


# Initialize login manager
login_manager = LoginManager()


# Create user loader function
@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)
