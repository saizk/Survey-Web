import datetime
import dateutil.tz

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
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

@bp.route("/results")
@login_required
def resultsview(survey_id):
    survey = model.Survey.query.filter_by(id=survey_id)
    return render_template("views/resultsview.html",  current_user=current_user, survey=survey)

@bp.route("/answerview")
@login_required
def answerview():
    return render_template("views/answerview.html",  current_user=current_user)

@bp.route("/create-survey", methods=["POST"])
@login_required
def createsurvey():
    title = request.form.get("survey_title")
    description = request.form.get("survey_desc")
    state = model.SurveyState.new
    timestamp = datetime.datetime.now(dateutil.tz.tzlocal())

    if not title:
        flash("")
        return redirect(url_for("views.createview"))

    new_survey = model.Survey(owner_id=session["user"], title=title, description=description, state=state, timestamp=timestamp)

    db.session.add(new_survey)
    db.session.commit()

    questions = request.form.getlist("question")
    question_objects = []
    for idx, question in enumerate(questions):
        question_type = model.QuestionType.NumberAnswer  #hardcoded
        new_question = model.Question(survey_id=new_survey.id, statement=question, question_type=question_type, position=idx+1)
        db.session.add(new_question)
        question_objects.append(new_question)
        
    db.session.commit()

    for i, new_question in enumerate(question_objects):
        options = request.form.getlist("answerfor%d" % i)
        for j, option in enumerate(options):
            new_option = model.QuestionOption(question_id=new_question.id, statement=option, position=j+1)
            db.session.add(new_option)
    
    db.session.commit()

    return redirect(url_for("views.surveyview"))




