from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class Survey(db.Model):
    __tablename__ = "surveys"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    start_date = db.Column(db.String, nullable=False)
    end_date = db.Column(db.String)
    user_id = db.Column(db.String, db.ForeignKey("users.id"), nullable=False)

class Question(db.Model):
    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String, nullable=False)
    note = db.Column(db.String)
    surv_id = db.Column(db.Integer, db.ForeignKey("surveys.id"), nullable=False)
    survey = db.relationship('Survey', backref='questions')


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=True, nullable=False)

