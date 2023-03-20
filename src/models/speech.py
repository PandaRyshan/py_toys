import sqlalchemy as sa

from ..db import db


class Speech(db.Model):

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id = sa.Column(sa.Integer)
    created_at = sa.Column(sa.DateTime, default=sa.func.now())
    filepath = sa.Column(sa.String(255), default="")
    desc = sa.Column(sa.String(255), default="")
    text = sa.Column(sa.Text, default="")
