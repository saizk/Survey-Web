import datetime
import dateutil.tz

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import model

bp = Blueprint("main", __name__)

@bp.route("/", methods=["GET"])
def index():

    # user = model.User(
    #     id = 9283,
    #     email="jambosergio@jamberson.com", 
    #     name="sech",
    #     password = "soyunjamboraro"
    #     )

    # surveys = [
    #     model.Survey(
    #         id = 331201,
    #         owner_id = user,
    #         title = "mi survey de puto noob",
    #         description= "aqui hago jamburas",
    #         state = 1,
    #         timestamp=datetime.datetime.now(dateutil.tz.tzlocal())            
    #     ),

    #     model.Survey(
    #         id = 331202,
    #         owner_id=user,
    #         title = "mi survey de puto noob2",
    #         description= "aqui hago jamburas2",
    #         state = 3,
    #         timestamp=datetime.datetime.now(dateutil.tz.tzlocal())            
    #     )
    # ]

    # questions = [
    #     model.Question(
    #         id = 2131,
    #         survey_id = surveys[0],
    #         statement = "olakease?",
    #         question_type = 1,
    #         position = 1 
    #     ),
    #     model.Question(
    #         id = 2132,
    #         survey_id = surveys[0],
    #         statement = "olakease?22222",
    #         question_type = 2,
    #         position = 2 
    #     )
    # ]

    # question_options = [
    #     model.QuestionOption(
    #         id = 21312,
    #         statement = "toi aki to chilin",
    #         position = 1
            
    #     ),
    #     model.QuestionOption(
    #         id = 213,
    #         statement = "comiendookease",
    #         position = 1
            
    #     )
    # ]

    # question_answers = [
    #     model.QuestionAnswer(
    #         id = 2131,
    #         answer_list= question_options[0]
            
    #     ),
    #     model.QuestionAnswer(
    #         id = 2132,
    #         answer_list = question_options
    #     )
    # ]

    # survey_answer = model.SurveyAnswer(
    #     id = 3432,
    #     survey_id = surveys[0],
    #     timestamp=datetime.datetime.now(dateutil.tz.tzlocal())        
    # )
    
    return render_template("main/index.html")


@bp.route("/profile")
def profile():
    return render_template("main/profile.html")