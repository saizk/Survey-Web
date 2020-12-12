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
        order_by="Survey.timestamp"
    )


# class Message(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     response_to_id = db.Column(db.Integer, db.ForeignKey('message.id'))
#     response_to = db.relationship('Message', backref='responses', remote_side=[id], lazy=True)

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


class QuestionType(enum.Enum):
    OneAnswer = 1
    ManyAnswers = 2
    TextAnswer = 3
    NumberAnswer = 4

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer,db.ForeignKey("survey.id"), nullable=False)
    statement = db.Column(db.String(1024), nullable=False)
    type = db.Column(db.Enum(QuestionType), nullable=False)
    position = db.Column(db.Integer, nullable=False)
    options = db.relationship(
        "QuestionOption",
        backref="option",
        lazy=True,
        cascade="all, delete-orphan",
        # order_by= ??
    )
    

class QuestionOption(db.Model):
    id = db.Column(db.Integer, primary_key=True)

class QuestionAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # ...
    answer_number = db.Column(db.Integer)
    # ...

class SurveyAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    timestamp = db.Column(db.DateTime(), nullable=False)