import datetime, dateutil.tz, hashlib

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from . import db, model


bp = Blueprint("views", __name__)

def survey_status_changer(survey, new_status):
    if new_status == "New":
        survey.state = model.SurveyState.new
    elif new_status == "Online":
        survey.state = model.SurveyState.online
    elif new_status == "Closed":
        survey.state = model.SurveyState.closed

@bp.route("/my-surveys", methods=["POST", "GET"])
@login_required
def surveys_view():

    if request.method == "POST":
        status = request.form.get("survey_status")
        survey = model.Survey.query.get(int(request.form.get("survey_id")))
        
        survey_status_changer(survey,status)
        db.session.commit()

    survey_list = model.Survey.query.filter_by(owner_id = current_user.id).all()
    survey_number = len(survey_list)

    answer_number = {}
    for survey in survey_list:
        answer_number[survey.id] = model.SurveyAnswer.query.filter_by(id = survey.id).count()

    status_list={}  
    for survey in survey_list:
        current_survey_state = model.Survey.query.filter_by(id = survey.id).first()
        status_list[survey.id] = current_survey_state.state.name

    return render_template("views/surveyview.html",current_user=current_user, survey_number=survey_number, survey_list=survey_list, answer_number=answer_number, status_list=status_list) 

@bp.route("/<survey_hash>/answer", methods=["POST", "GET"])
def create_answer(survey_hash):
    selected_survey = model.Survey.query.filter_by(survey_hash=survey_hash).first()

    # Checks for empty question fields
    questions = request.form.getlist("question")
    for q_idx in range(len(questions)):
        selected_ans_options = request.form.getlist("ans_q%d" % (q_idx+1))
        if not selected_ans_options:
            flash("Answer %d is empty" % (q_idx+1))
            return redirect(url_for("views.display_public_server", survey_hash=selected_survey.survey_hash))
    
    new_survey_answer = model.SurveyAnswer(survey_id=selected_survey.id, timestamp=datetime.datetime.now(dateutil.tz.tzlocal()))

    survey_questions = model.Question.query.filter_by(survey_id=selected_survey.id).all()
    print("Survey_questions", survey_questions)
    for q_idx, question in enumerate(survey_questions):
        
        selected_ans_options = request.form.getlist("ans_q%d" % (q_idx+1))
        print("Selected options:", selected_ans_options)

        if question.question_type.name == "TextAnswer":
            text = selected_ans_options[0]
            print("text:", text)
        elif question.question_type.name == "NumberAnswer":
            number = int(selected_ans_options[0])
            print("number", number)
        else:
            text, number = None, None
        
        for a_idx, ans_statement in enumerate(selected_ans_options):
            ans_options = model.QuestionOption.query.filter_by(question_id=question.id, position=a_idx+1).all()
            print("ans_options", ans_options)
            for ans_option in ans_options:
                new_question_answer = model.QuestionAnswer(
                                        text=text, number=number,
                                        answered_question_id = question.id,
                                        question_option_id=ans_option.id,
                                        answer_id=selected_survey.id
                                    )
                if text:
                    text = None
                if number:
                    number = None
                db.session.add(new_question_answer)
                db.session.commit()
    
    db.session.add(new_survey_answer)
    db.session.commit()

    return render_template("main/index.html",  current_user=current_user)

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

@bp.route("/create-survey")
@login_required
def create_view():
    return render_template("views/createview.html", current_user=current_user)

@bp.route("/create-survey/send", methods=["POST", "GET"])
@login_required
def create_survey():
    title = request.form.get("survey_title")
    description = request.form.get("survey_desc")
    # Checks if survey has a title
    if not title:
        flash("A survey cannot be created without a title")
        return redirect(url_for("views.create_view"))
    
    enc_str = str(current_user.id)+title+description
    survey_hash = hashlib.md5((enc_str).encode('utf-8')).hexdigest()
    
    new_survey = model.Survey(owner_id=current_user.id, title=title,
                              description=description, state=model.SurveyState.new,
                              timestamp=datetime.datetime.now(dateutil.tz.tzlocal()),
                              survey_hash=survey_hash
                )
    db.session.add(new_survey)
    db.session.commit()

    # Checks for empty questions and possible answers
    questions = request.form.getlist("question")
    print("Questions", questions)
    if not questions or any(not q for q in questions):  # ["", "", ...]
        flash("Cannot create a survey with empty questions")
        return redirect(url_for("views.create_view"))
    for i in range(len(questions)):
        ans_options = request.form.getlist("answerfor%d" % i)

    for idx, question in enumerate(questions):
        qrawtype = request.form.get("question_type%d" % idx)
        question_type = question_mapper(qrawtype)
        position = request.form.get("num_q%d" % idx)
        new_question = model.Question(survey_id=new_survey.id, statement=question, question_type=question_type, position=int(position))
        db.session.add(new_question)
    db.session.commit()

    question_objects = model.Question.query.filter_by(survey_id=new_survey.id).all()
    for q_idx, new_question in enumerate(question_objects):
        
        ans_options = request.form.getlist("answerfor%d" % q_idx)
        for a_idx, ans_option in enumerate(ans_options):
            # Fixes JS bug a question type changes from those which accept possible answers (1-Ans & Many-Ans)
            # and those which do not (Text & Num)
            if new_question.question_type.name == "OneAnswer" or new_question.question_type.name == "ManyAnswers":
                statement = ans_option
            else:
                statement = None

            new_ans_option = model.QuestionOption(question_id=new_question.id, statement=statement, position=(a_idx+1))
            db.session.add(new_ans_option)
    db.session.commit()

    return redirect(url_for("views.surveys_view"))

@bp.route("/my-surveys/<survey_hash>/addquestion")
@login_required
def add_question_view(survey_hash):
    selected_survey = model.Survey.query.filter_by(survey_hash=survey_hash).first()
    return render_template("views/editview.html", selected_survey=selected_survey)

@bp.route("/my-surveys/<survey_hash>/addquestion", methods=["POST", "GET"])
@login_required
def add_question(survey_hash):
    selected_survey = model.Survey.query.filter_by(survey_hash=survey_hash).first()

    # Checks for empty question fields
    questions = request.form.getlist("question")
    print(questions)
    if not questions or any(len(q) == 0 for q in questions):  # ["", "", ...]
        flash("Empty questions cannot be added to a survey")
        return redirect(url_for("views.add_question_view", survey_hash=selected_survey.survey_hash))

    num_question =  model.Question.query.filter_by(survey_id=selected_survey.id).count() # position
    print(num_question, type(num_question))
    for idx, question in enumerate(questions):
        qrawtype = request.form.get("question_type%d" % idx)
        question_type = question_mapper(qrawtype)
        new_question = model.Question(survey_id=selected_survey.id, statement=question, question_type=question_type, position=int(num_question)+1)
        db.session.add(new_question)
        db.session.commit()
    return redirect(url_for("views.display_survey", survey_hash=selected_survey.survey_hash))

@bp.route("/my-surveys/<survey_hash>")
@login_required
def display_survey(survey_hash):
    selected_survey = model.Survey.query.filter_by(survey_hash=survey_hash).first()
    questions = model.Question.query.filter_by(survey_id=selected_survey.id).order_by("position").all()
    question_list =  [(question, model.QuestionOption.query.filter_by(question_id=question.id).all()) 
                      for question in questions]
    return render_template("views/answerview.html",  current_user=current_user, selected_survey=selected_survey, info=question_list)

@bp.route("/<survey_hash>")
def display_public_survey(survey_hash):
    selected_survey = model.Survey.query.filter_by(survey_hash=survey_hash).first_or_404()
    questions = model.Question.query.filter_by(survey_id=selected_survey.id).order_by("position").all()
    answers = model.SurveyAnswer.query.filter_by(survey_id=selected_survey.id).all()

    answer_list = [(answer, )
                    for answer in answers]
    question_list =  [(question, model.QuestionOption.query.filter_by(question_id=question.id).all()) 
                      for question in questions]
    return render_template("views/answerview.html", selected_survey=selected_survey, info=question_list, answers=answers)


@bp.route("/<survey_hash>/results")
@login_required
def resultsview(survey_hash):
    selected_survey = model.Survey.query.filter_by(survey_hash=survey_hash).first()
    return render_template("views/resultsview.html",  current_user=current_user, survey=selected_survey)