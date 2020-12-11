import enum
from flask_login import UserMixin
from . import db

# UserMixin will add Flask login attributes to the model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    surveys = db.relationship(
        "Survey",
        backref="user",
        lazy=True,  # select
        # cascade="all, delete-oprhan",
        # order_by="Survey.position"
    )
    # messages = db.relationship(
    #     'Message',
    #     backref='user',
    #     lazy=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    response_to_id = db.Column(db.Integer, db.ForeignKey('message.id'))
    response_to = db.relationship('Message', backref='responses', remote_side=[id], lazy=True)

class SurveyState(enum.Enum):
    new = 1,
    online = 2
    closed = 3

class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(128), nullable=True)
    state = db.Column(db.Enum(SurveyState), nullable=False)
    timestamp = db.Column(db.DateTime(), nullable=False)
    questions = db.relationship(
        "Question",
        backref="survey",
        lazy=True,
        cascade="all, delete-oprhan",
        order_by="Question.position"
    )

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    survey_id = db.Column(db.Integer,db.ForeignKey("survey.id"), nullable=False)


# class QuestionOption(Question):
#     pass

class QuestionAnswer(db.Model):
    # ...
    answer_number = db.Column(db.Integer)
    # ...

# class SurveyAnswer(Survey):
#     timestamp = db.Column(db.DateTime(), nullable=False)