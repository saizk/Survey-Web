import enum
from flask_login import UserMixin
from . import db

# UserMixin will add Flask login attributes to the model
class User(UserMixin, db.Model):
    # __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    surveys = db.relationship(
        "Survey",
        backref="user",
        lazy=True,  # select
        cascade="all, delete-orphan",
        order_by="Survey.timestamp",
    )


class SurveyState(enum.Enum):
    new = 1
    online = 2
    closed = 3

class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(512), nullable=True)
    state = db.Column(db.Enum(SurveyState), nullable=False)
    timestamp = db.Column(db.DateTime(), nullable=False)

    questions = db.relationship(
        "Question",
        backref="survey",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="Question.position"
    )
    answers = db.relationship(
        "SurveyAnswer",
        backref="survey",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="Question.position"
    )

class QuestionType(enum.Enum):
    OneAnswer = 1
    ManyAnswers = 2
    TextAnswer = 3
    NumberAnswer = 4

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer,db.ForeignKey("survey.id"), nullable=False)
    
    statement = db.Column(db.String(1024), nullable=False)
    question_type = db.Column(db.Enum(QuestionType), nullable=False)
    position = db.Column(db.Integer, nullable=False)

    options = db.relationship(
        "QuestionOption",
        backref="question",
        lazy=True,
        cascade="all, delete-orphan",
        # order_by= ??
    )

    

class QuestionOption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer,db.ForeignKey("question.id"), nullable=False)
    statement = db.Column(db.String(1024), nullable=False)
    position = db.Column(db.Integer, nullable=False)


class QuestionAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer,db.ForeignKey("question.id"), nullable=False)

    question_option_id = db.Column(db.Integer,db.ForeignKey("question_option.id"), nullable=False)
    answer_list = db.relationship(  # single/multiple choice
        "QuestionOption",
        backref="QuestionAnswer",
        lazy=True,
        # cascade="delete-orphan",
    )

    answer_text = db.Column(db.String(1024)) # QuestionType 3
    answer_number = db.Column(db.Integer) # QuestionType 4


class SurveyAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    survey_id = db.Column(db.Integer, db.ForeignKey("survey.id"), nullable=False) 
    timestamp = db.Column(db.DateTime(), nullable=False)
    answer_id = db.Column(db.Integer, db.ForeignKey("question_answer.id"), nullable=False)
    answers = db.relationship(
        "QuestionAnswer",
        backref="SurveyAnswer",
        lazy=True,
        # cascade="all, delete-orphan",
        # order_by="Question.position"
    )