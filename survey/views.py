import datetime
import dateutil.tz

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import db, model

from sqlalchemy import func

bp = Blueprint("views", __name__)

@bp.route("/my-surveys")
@login_required
def surveyview():
    survey_number = len(model.Survey.query.filter_by(owner_id = current_user.id).all())
    return render_template("views/surveyview.html",  current_user=current_user, survey_number=survey_number)

@bp.route("/create-survey")
@login_required
def createview():
    return render_template("views/createview.html",  current_user=current_user)
    

@bp.route("/create-survey", methods=["POST"])
@login_required
def createsurvey():
    title = request.form.get("survey_title")
    description = request.form.get("survey_desc")
    state = model.SurveyState.new
    timestamp = datetime.datetime.now(dateutil.tz.tzlocal())
    questions = request.form.get("question0") # Example
    # questions = request.form.getlist("question_list")
    
    new_survey = model.Survey(title=title, description=description, state=state, timestamp=timestamp)

    for question in questions:
        new_question = model.Question(question_id = question.id, statement=question, question_type=1)

    if not title:
        flash("")
        return redirect(url_for("views.createview"))

    db.session.add(new_survey)
    db.session.commit()
    return redirect(url_for("views.surveyview", questions=questions))


@bp.route("/results")
@login_required
def resultsview(survey_id):
    survey = model.Survey.query.filter_by(id=survey_id)
    return render_template("views/resultsview.html",  current_user=current_user, survey=survey)

@bp.route("/answerview")
@login_required
def answerview():
    return render_template("views/answerview.html",  current_user=current_user)



