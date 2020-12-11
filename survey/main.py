import datetime
import dateutil.tz

from flask import Blueprint, render_template
from flask_login import login_required, current_user
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
    return render_template("main/index.html", current_user=current_user)

@bp.route("/profile")
@login_required
def profile():
    return render_template("main/profile.html", name=current_user.name)
