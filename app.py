from flask import Flask, flash, redirect, render_template, render_template_string, request, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class User(db.Model):
    username = db.Column(db.String(), nullable=False)
    id = db.Column(db.Integer, primary_key=True)

@app.route("/")
def home():
    if session.get("user_id") == None:
        return redirect("/login")


@app.route("/login")
def login():
    if session.get("user_id") != None:
        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        if session.get("user_id") != None:
            return redirect("/")
        return render_template("register.html")
    else:
        phone_number = request.form["phone_number"]
        person = User(username=phone_number)
        db.session.add(person)
        db.session.commit()
        return render_template("dummy.html", phone_number=phone_number)