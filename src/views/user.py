from models.user import User
from flask import render_template
from flask import Blueprint
from src.db import db


bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/login")
def login():
    return render_template("user/login.html")


@bp.route("/logout")
def logout():
    return "Logout"


@bp.route("/list")
def user_list():
    users = db.session.execute(db.select(User).order_by(User.username)).scalars().all()
    return render_template("user/list.html", users=users)
