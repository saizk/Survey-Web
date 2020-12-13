import datetime
import dateutil.tz

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import model

bp = Blueprint("views", __name__)

@bp.route("/my-surveys")
@login_required
def surveyview():
    return render_template("views/surveyview.html",  current_user=current_user, num_surveys=0)

@bp.route("/create-survey")
@login_required
def createview():
    return render_template("views/createview.html",  current_user=current_user, name=current_user.name)

@bp.route("/create-survey", methods=["POST"])
@login_required
def createsurvey():
    title = request.form.get("survey_title")
    description = request.form.get("survey_description")
    state = model.SurveyState.new
    timestamp = datetime.datetime.now(dateutil.tz.tzlocal())

    questions = None

    new_survey = model.User(title=title, description=description, state=state, timestamp=timestamp, questions=questions)

    return redirect(url_for("views.surveyview"))



@bp.route("/resultsview")
@login_required
def resultsview():
    return render_template("views/resultsview.html",  current_user=current_user)

@bp.route("/answerview")
@login_required
def answerview():
    return render_template("views/answerview.html",  current_user=current_user)