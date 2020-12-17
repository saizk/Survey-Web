
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
def survey_view():
    survey_query = model.Survey.query.filter_by(owner_id = current_user.id)
    survey_list = survey_query.all()
    survey_number = survey_query.count()
    question_list = [model.Question.query.filter_by(survey_id=survey.id).all()
                      for survey in survey_list]
    # answer_list = [[(question.id, model.SurveyAnswer.query.filter_by(question_id = question.id).count()) for question in survey] for survey in question_list]

    return render_template("views/surveyview.html",  current_user=current_user, survey_number=survey_number, survey_list=survey_list)

@bp.route("/my-surveys/survey<int:survey_id>")
@login_required
def display_survey(survey_id):
    selected_survey = model.Survey.query.filter_by(id=survey_id).first()
    questions = model.Question.query.filter_by(survey_id=survey_id).order_by("position").all()
    question_list =  [(question, model.QuestionOption.query.filter_by(question_id=question.id).all()) 
                      for question in questions]
    return render_template("views/answerview.html",  current_user=current_user, selected_survey=selected_survey, info=question_list)

@bp.route("/survey/<survey_hash>")
def display_public_survey(survey_hash):
    selected_survey = model.Survey.query.filter_by(survey_hash=survey_hash).first()
    questions = model.Question.query.filter_by(survey_id=selected_survey.id).order_by("position").all()
    question_list =  [(question, model.QuestionOption.query.filter_by(question_id=question.id).all()) 
                      for question in questions]
    return render_template("views/answerview.html", selected_survey=selected_survey, info=question_list)

@bp.route("/create-survey")
@login_required
def create_view():
    return render_template("views/createview.html", current_user=current_user)

@bp.route("/survey/<survey_hash>/answer", methods=["POST", "GET"])
def create_answer(survey_hash):
    selected_survey = model.Survey.query.filter_by(survey_hash=survey_hash).first()

    new_survey_answer = model.SurveyAnswer(survey_id=selected_survey.id, timestamp=datetime.datetime.now(dateutil.tz.tzlocal()))

    db.session.add(new_survey_answer)

    survey_questions = model.Question.query.filter_by(survey_id=selected_survey.id).all()
    print("Survey_questions", survey_questions)

    for idx, question in enumerate(survey_questions):
        if question.question_type.name == "TextAnswer":
            text = request.form.get("ans_q%d" % idx)
            print(text)
        elif question.question_type.name == "NumberAnswer":
            number = request.form.get("ans_q%d" % idx)
            print(number)
        # else:
        selected_ans_options = request.form.getlist("ans_q%d" % idx)
        print("Selected options:", selected_ans_options)
        for ans_option in selected_ans_options:
            print(ans_option)
            new_question_answer = model.QuestionAnswer(
                                    answered_question_id = question.id,
                                    question_option_id=ans_option.id,
                                    answer_id=selected_survey.id
                                )
            db.session.add(new_question_answer)
    db.session.commit()

    return render_template("main/index.html",  current_user=current_user)

@bp.route("/results")
@login_required
def resultsview(survey_id):
    survey = model.Survey.query.filter_by(id=survey_id)
    return render_template("views/resultsview.html",  current_user=current_user, survey=survey)

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
def create_survey():
    title = request.form.get("survey_title")
    description = request.form.get("survey_desc")
    state = model.SurveyState.new
    timestamp = datetime.datetime.now(dateutil.tz.tzlocal())

    enc_str = str(current_user.id)+title+description
    survey_hash = hashlib.md5((enc_str).encode('utf-8')).hexdigest()
    
    new_survey = model.Survey(owner_id=current_user.id, title=title, description=description, state=state, timestamp=timestamp, survey_hash=survey_hash)

    if not title:
        flash("Cannot submit survey")
        return redirect(url_for("views.create_view"))

    db.session.add(new_survey)
    db.session.commit()

    questions = request.form.getlist("question")
    if not questions:
        flash("Cannot submit survey")
        return redirect(url_for("views.create_view"))

    question_objects = []

    for idx, question in enumerate(questions):
        qrawtype = request.form.get("question_type%d" % idx)
        question_type = question_mapper(qrawtype)
        position = request.form.get("num_q%d" % idx)
        new_question = model.Question(survey_id=new_survey.id, statement=question, question_type=question_type, position=int(position))
        db.session.add(new_question)
        question_objects.append(new_question)
    
    db.session.commit()

    for i, new_question in enumerate(question_objects):
        ans_options = request.form.getlist("answerfor%d" % i)
        for j, ans_option in enumerate(ans_options):
            new_ans_option = model.QuestionOption(question_id=new_question.id, statement=ans_option, position=j+1)
            db.session.add(new_ans_option)
    
    db.session.commit()

    return redirect(url_for("views.survey_view"))