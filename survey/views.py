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
    survey_list = model.Survey.query.filter_by(owner_id = current_user.id).all()
    survey_number = len(survey_list)
    for survey in survey_list:
        return render_template("views/surveyview.html",  current_user=current_user, survey_number=survey_number, survey_id = survey.id)

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
    # questions = request.form.get("question0") # Example
    questions = request.form.getlist("question_list")
    
    if not title:
        flash("")
        return redirect(url_for("views.createview"))

    new_survey = model.Survey(owner_id=current_user.id, title=title, description=description, state=state, timestamp=timestamp)
    db.session.add(new_survey)
    db.session.commit()

    for question in questions:
        new_question = model.Question(survey_id=new_survey.id, statement=question, question_type=1)

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



