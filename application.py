from flask import Flask, request, jsonify, session
from flask_session import Session
from flask_bcrypt import Bcrypt
from models import *
from flask_marshmallow import Marshmallow
import json, re

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Surv.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Link the Flask app with the database (no Flask app is actually being run yet).
db.init_app(app)
ma = Marshmallow(app)
# Configure Password hashing
My_bcrypt = Bcrypt(app)

class SurveySchema(ma.ModelSchema):
    class Meta:
        model = Survey

class QuestionSchema(ma.ModelSchema):
    class Meta:
        model = Question


@app.route("/")
def index():
    return ("Server is running ...")

@app.route("/survey", methods = ["GET","POST"])
def survey():
    if session.get("user") is None:
        return "Please Login First"
    if (request.method == "GET"):
        all_surveys=Survey.query.all()
        Surv_schema = SurveySchema(many=True)
        output = Surv_schema.dump(all_surveys)#.data

        for sur in output:
            related_questions = Question.query.with_entities(Question.body, Question.note).filter_by(surv_id=sur["id"]).all()
            Ques_schema = QuestionSchema(many=True)
            ques_output = Ques_schema.dump(related_questions)
            sur["questions"] = ques_output
        return jsonify(output)

    #POST
    body = json.loads(request.data)
    if re.match(r"^\d{2}/\d{2}/\d{4} \d{2}:\d{2}$", body["start_data"]) and re.match(r"^\d{2}/\d{2}/\d{4} \d{2}:\d{2}$", body["end_data"]):
        Survey2add = Survey(name=body["name"], description=body["description"], start_date=body["start_data"], end_date=body["end_data"], user_id = session['user'].id)
        db.session.add(Survey2add)
        for ques in body["questions"]:
            Ques2add = Question(body=ques["body"], note=ques["note"], survey = Survey2add)
            db.session.add(Ques2add)
        db.session.commit()
        return ("Survey {} added successfuly".format(body['name']))
    return ("Dates are not inserted in proper format")

@app.route("/Register", methods = ["POST"])
def register():
    body = json.loads(request.data)
    username = body.get("username")
    password1 = body.get("password")
    password2 = body.get("password_confirm")
    username_srch = User.query.filter_by(username=username).first()
    if(username_srch != None):
        return ("Registartion Failed: User name already exists")

    elif(password1 != password2):
        return ("Registartion Failed: Passwords doesn't match")

    else:
        pw_hash = My_bcrypt.generate_password_hash(password1).decode('utf-8')
        user2add = User(username=username, password=pw_hash)
        db.session.add(user2add)
        db.session.commit()
        return "Registration Completed, Login to start using the Survey APIs"

@app.route('/Login', methods = ["POST"])
def login():
    body = json.loads(request.data)
    username = body.get("username")
    password = body.get("password")
    user_srch = User.query.filter_by(username=username).first()
    if (user_srch == None):
        return "Login Failed: username doesn't exist"
    elif(My_bcrypt.check_password_hash(user_srch.password, password) == False):
        return "Login Failed: username and password don't match"
    else:
        session['user'] = user_srch
        return "Login succeeded"


if __name__ == '__main__':
    app.run(debug=True)
    app.run()