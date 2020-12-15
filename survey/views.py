
import datetime
import dateutil.tz

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from . import db, model

import hashlib

from sqlalchemy import func

bp = Blueprint("views", __name__)

@bp.route("/my-surveys")
@login_required
def surveyview():
    survey_list = model.Survey.query.filter_by(owner_id = current_user.id).all()
    return render_template("views/surveyview.html", current_user=current_user, surveys=survey_list, survey_number=len(survey_list))

@bp.route("/my-surveys/survey<int:survey_id>")
@login_required
def displaysurvey(survey_id):
    selected_survey = model.Survey.query.filter_by(id=survey_id).first()
    questions = model.Question.query.filter_by(survey_id=survey_id).all()
    my_list =  [(question, model.QuestionOption.query.filter_by(question_id=question.id).all()) 
                for question in questions]
    print(my_list)
    return render_template("views/answerview.html",  current_user=current_user, selected_survey=selected_survey, info=my_list)


@bp.route("/survey/<survey_hash>")
def display_public_survey(survey_hash):
    selected_survey = model.Survey.query.filter_by(survey_hash=survey_hash).first()
    questions = model.Question.query.filter_by(survey_id=selected_survey.id).all()
    my_list =  [(question, model.QuestionOption.query.filter_by(question_id=question.id).all()) 
                for question in questions]
    return render_template("views/answerview.html",  current_user=current_user, selected_survey=selected_survey, info=my_list)


@bp.route("/create-survey")
@login_required
def createview():
    return render_template("views/createview.html", current_user=current_user)

@bp.route("/results")
@login_required
def resultsview(survey_id):
    survey = model.Survey.query.filter_by(id=survey_id)
    return render_template("views/resultsview.html",  current_user=current_user, survey=survey)

@bp.route("/answerview")
@login_required
def answerview():
    return render_template("views/answerview.html",  current_user=current_user)


def question_mapper(value):
    if value == "one":
        return(model.QuestionType.OneAnswer)
    elif value == "mult":
        return(model.QuestionType.ManyAnswers)
    elif value == "text":
        return(model.QuestionType.TextAnswer)
    elif value == "num":
        return(model.QuestionType.NumberAnswer)
    return -1

@bp.route("/create-survey", methods=["POST"])
@login_required
def createsurvey():
    title = request.form.get("survey_title")
    description = request.form.get("survey_desc")
    state = model.SurveyState.new
    timestamp = datetime.datetime.now(dateutil.tz.tzlocal())
    survey_hash = hashlib.md5((str(current_user.id)+title+description).encode('utf-8')).hexdigest()
    
    new_survey = model.Survey(owner_id=current_user.id, title=title, description=description, state=state, timestamp=timestamp, survey_hash=survey_hash)

    if not title:
        flash("Cannot submit survey")
        return redirect(url_for("views.createview"))

    db.session.add(new_survey)
    db.session.commit()

    questions = request.form.getlist("question")
    question_objects = []

    for idx, question in enumerate(questions):
        qrawtype = request.form.get("question_type%d" % idx)
        question_type = question_mapper(qrawtype)

        new_question = model.Question(survey_id=new_survey.id, statement=question, question_type=question_type, position=idx+1)
        db.session.add(new_question)
        question_objects.append(new_question)
    
    # if not questions:
    #     flash("Cannot submit survey")
    #     return redirect(url_for("views.createview"))

    db.session.commit()

    for i, new_question in enumerate(question_objects):
        options = request.form.getlist("answerfor%d" % i)
        for j, option in enumerate(options):
            new_option = model.QuestionOption(question_id=new_question.id, statement=option, position=j+1)
            db.session.add(new_option)
    
    db.session.commit()

    

    return redirect(url_for("views.surveyview"))