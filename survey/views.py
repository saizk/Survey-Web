import datetime
import dateutil.tz

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import model

bp = Blueprint("views", __name__)

@bp.route("/mainview")
@login_required
def mainview():
    return render_template("views/mainview.html", current_user=current_user, num_surveys=0)

@bp.route("/surveyview")
@login_required
def surveyview():
    return render_template("views/surveyview.html",  current_user=current_user)

@bp.route("/surveyview", methods=["POST"])
@login_required
def surveypost():
    title = request.form.get("title")
    return redirect(url_for("views.surveyview"))

@bp.route("/resultsview")
@login_required
def resultsview():
    return render_template("views/resultsview.html",  current_user=current_user)

@bp.route("/answerview")
@login_required
def answerview():
    return render_template("views/answerview.html",  current_user=current_user)