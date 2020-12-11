from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    messages = db.relationship('Message', backref='user', lazy=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.String(512), nullable=False)
    timestamp = db.Column(db.DateTime(), nullable=False)
    response_to_id = db.Column(db.Integer, db.ForeignKey('message.id'))
    response_to = db.relationship('Message', backref='responses', remote_side=[id], lazy=True)

# class Survey(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     owner_id = db.Column(db.Integer, db.ForeignKey(user.id), nullable=False)
#     title = db.Column(db.String(64), nullable=False)
#     description = db.Column(db.String(128), nullable=True)
#     # state = db.Column(*******, nullable=False)
#     timestamp = db.Column(db.DateTime(), nullable=False)

# class Question(db.Model):
#     id = db.Column(db.Integer, primary_key=True)


# # class QuestionOption(Question):
# #     pass

# # class QuestionAnswer(Question):
# #     pass

# class SurveyAnswer(Survey):
#     timestamp = db.Column(db.DateTime(), nullable=False)