import datetime
import dateutil.tz

from flask import Blueprint, render_template
from . import model

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    # user = model.User(email="mary@example.com", name="mary")
    # posts = [
    #     model.Message(
    #         user=user,
    #         text="Test post",
    #         timestamp=datetime.datetime.now(dateutil.tz.tzlocal()),
    #     ),
    #     model.Message(
    #         user=user,
    #         text="Another post",
    #         timestamp=datetime.datetime.now(dateutil.tz.tzlocal()),
    #     ),
    # ]
    # return render_template("main/index.html", posts=posts)
    return render_template("main/index.html")

@bp.route("/profile")
def profile():
    return render_template("main/profile.html")
