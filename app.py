from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from sklearn.neighbors import KNeighborsClassifier
import cv2
from win32com.client import Dispatch
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime
import os
import time
import pyttsx3
from flask import Flask, render_template, request, jsonify

from dotenv import load_dotenv
import os
import pathlib
import textwrap


import google.generativeai as genai
from IPython.display import Markdown

db = SQLAlchemy()
app = Flask(__name__)
app.config['SECRET_KEY'] = "my-secrets"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///video-meeting.db"
db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)
student_data=[["Sree charan",3,"Dsa Html Python","i am very hard working guy","../static/student/1.avif",150,"26-05-2004"],
                ["Ritik Kumar ",4,"Dsa Html Python Js","i am very hard working guy","../static/student/2.avif",150,"27-05-2004"],
                ["Amit kumar",1,"Dsa","i am very hard working guy","../static/student/3.avif",150,"26-05-2004"],
                ["Rohan",3,"Dsa Html Python","i am very hard working guy","../static/student/4.avif",150,"26-05-2004"],
                ["yagnesh",3,"Dsa Html Python","i am very hard working guy","../static/student/5.avif",150,"26-05-2004"]]
meassby=[]
@login_manager.user_loader
def load_user(user_id):
    return Register.query.get(int(user_id))


class Register(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    python = db.Column(db.Integer,nullable=True)
    dsa=db.Column(db.Integer,nullable=True)
    html=db.Column(db.Integer,nullable=True)
    total=db.Column(db.Integer,nullable=True)
    cat=db.Column(db.Integer,nullable=True)
    def is_active(self):
        return True

    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        return True


with app.app_context():
    db.create_all()


class RegistrationForm(FlaskForm):
    email = EmailField(label='Email', validators=[DataRequired()])
    first_name = StringField(label="First Name", validators=[DataRequired()])
    last_name = StringField(label="Last Name", validators=[DataRequired()])
    username = StringField(label="Username", validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField(label="Password", validators=[DataRequired(), Length(min=8, max=20)])


class LoginForm(FlaskForm):
    email = EmailField(label='Email', validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])


@app.route("/")
def home():
    return redirect(url_for("login"))




@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = Register.query.filter_by(email=email, password=password).first()
        if user:
            login_user(user)
            '''def face():

                def speak(str1):
                    speak = Dispatch("SAPI.SpVoice")
                    speak.Speak(str1)

                video = cv2.VideoCapture(0)
                facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

                with open('data/names.pkl', 'rb') as w:
                    LABELS = pickle.load(w)
                with open('data/faces_data.pkl', 'rb') as f:
                    FACES = pickle.load(f)

                print('Shape of Faces matrix --> ', FACES.shape)

                knn = KNeighborsClassifier(n_neighbors=5)
                knn.fit(FACES, LABELS)

                COL_NAMES = ['NAME', 'TIME']

                while True:
                    name="sree"
                    ret, frame = video.read()
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    faces = facedetect.detectMultiScale(gray, 1.3, 5)
                    for (x, y, w, h) in faces:
                        crop_img = frame[y:y + h, x:x + w, :]
                        resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
                        output = knn.predict(resized_img)
                        ts = time.time()
                        date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
                        timestamp = datetime.fromtimestamp(ts).strftime("%H:%M-%S")
                        exist = os.path.isfile("Attendance/Attendance_" + date + ".csv")
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 2)
                        cv2.rectangle(frame, (x, y - 40), (x + w, y), (50, 50, 255), -1)
                        cv2.putText(frame, str(output[0]), (x, y - 15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 1)
                        attendance = [str(output[0]), str(timestamp)]

                    cv2.imshow("Frame", frame)
                    k = cv2.waitKey(1)
                    if k == ord('o'):

                        if str(output[0]) in ["sree"]:
                            cv2.putText(frame, "Matched", (x, y - 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                            speak("Successfully logged in..")
                            return True
                        else:
                            speak("Wrong user Face detection not matched")
                            return False
                    if k == ord('q'):
                        break
                video.release()
                cv2.destroyAllWindows()
'''

            return render_template("index.html")


    return render_template("login.html", form=form)


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    flash("You have been logged out successfully!", "info")
    return redirect(url_for("login"))


os.getenv("AIzaSyDlkm2O5f7aujVl__OZEf3j50lP0HK4vnE")
genai.configure(api_key="AIzaSyDlkm2O5f7aujVl__OZEf3j50lP0HK4vnE")
@app.route("/All_students.html")
def all_students():
    return render_template("All_students.html",len=len(student_data),student_data=student_data)


def get_gemini_response(question):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(question)
    s = response.text
    text = s.replace('**', '\n')
    text = text.replace('*', " ")

    return text
@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    msq = "If this qustion is relate to study this is whishes then say yes or no   and  " + input + "first give  just yes or no not any thing not give any other answer except yes or no keep it in mind"
    y = get_gemini_response(msq)
    print(y)
    if ("Yes" in y):
        return get_gemini_response(input)
    else:

        return "We Will only answere which is related to Education"


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegistrationForm()
    if request.method == "POST" and form.validate_on_submit():
        new_user = Register(
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            password=form.password.data
        )
        db.session.add(new_user)
        db.session.commit()


        flash("Account created Successfully! <br>You can now log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html", form=form)



@app.route("/dashboard.html")

def dashboard():

    return render_template("dashboard.html", first_name=current_user.first_name, last_name=current_user.last_name)
@app.route("/"
           ""
           ".html")
def index():
    return render_template('chat.html')
@app.route("/meeting")

def meeting():
    return render_template("meeting.html", username=current_user.username)
@app.route("/E-Books.html")
def E_Books():
    return render_template("E-Books.html")



@app.route("/join", methods=["GET", "POST"])

def join():
    if request.method == "POST":
        room_id = request.form.get("roomID")
        return redirect(f"/meeting?roomID={room_id}")

    return render_template("join.html")


@app.route("/feedback.html")
def feedback():
    return render_template("feedback.html")

@app.route("/index.html")
def index1():
  return  render_template("index.html")
@app.route("/learn.html")
def learn():
      return render_template("learn.html",first_name=current_user.first_name, last_name=current_user.last_name,python=current_user.python,html=current_user.html,dsa=current_user.dsa,total=current_user.total)
@app.route("/Jobs.html")
def jobs():
    return render_template("Jobs.html")
@app.route("/assessement.html")
def assessment():
  return render_template("assessement.html")
@app.route("/Courses.html")
def Courses():
  return  render_template("Courses.html")
@app.route("/dsa.html")
def dsa():
    return render_template("dsa.html")
@app.route("/Skill_Tracks.html")
def Skill_Tracks():
    return render_template("Skill_Tracks.html")
@app.route("/Carrer_Tracks.html")
def Carrer_Tracks():
    return render_template("Carrer_Tracks.html")
@app.route("/Paid.html")
def Paid():
    return render_template("Paid.html")
@app.route("/quiz/bootstrap.html")
def boot():
    return render_template("quiz/bootstrap.html")
@app.route("/quiz/c.html")
def c():
    return render_template("quiz/c.html")
@app.route("/quiz/cpp.html")
def cpp():
    return render_template("quiz/cpp.html")
@app.route("/quiz/java.html")
def java():
    return render_template("quiz/java.html")

@app.route("/quiz/javascript.html")
def javascript():
    return render_template("quiz/javascript.html")
@app.route("/quiz/python.html")
def python():
    return render_template("quiz/python.html")
@app.route("/cheatsheet/cheat_c.html")
def cheat_c():
    return render_template("cheatsheet/cheat_c.html")
@app.route("/cheatsheet/cheat_html.html")
def cheat_html1():
    return render_template("cheatsheet/cheat_html.html")
@app.route("/cheatsheet/cheat_python.html")
def cheat_python():
    return render_template("cheatsheet/cheat_python.html")
@app.route("/cheatsheet/cheatsheet_html.html")
def cheat_html():
    return render_template("cheatsheet/cheatsheet_html.html")
@app.route("/cheatsheet/cheat_css3.html")
def cheat_css3():
    return render_template("cheatsheet/cheat_css3.html")
@app.route("/cheatsheet/cheat_java.html")
def cheat_java():
    return render_template("cheatsheet/cheat_java.html")
@app.route("/videos/video_c.html")
def video_c():
    return render_template("videos/video_c.html")

@app.route("/videos/video_python.html")
def video_python():
    return render_template("videos/video_python.html")
@app.route("/t-profilepage.html")
def t_profile():
    return render_template("t-profilepage.html")
if __name__ == '__main__':

  app.run(host='0.0.0.0', debug=True)
  
