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
    email = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
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
        if int(request.form['Test']) == 1:
            if request.form["Email"] == "" or request.form['Password'] == "":
                return render_template("register.html", error="Email or password missing")
            Email = request.form["Email"]
            Password = request.form['Password']
            person = User(email=Email, password=Password, username="Default" + str(db.session.query(User).count()))
            db.session.add(person)
            db.session.commit()
            return render_template("dummy.html", error="", id=str(db.session.query(User.id).filter(User.email == Email, User.password == Password).all()[0].id))
        else:
            if db.session.query(User).filter(User.username == request.form['Username']).count() >= 1:
                return render_template("dummy.html", error="Username already taken.")
            if len(request.form['Username']) > 60:
                return render_template("dummy.html", error="Please pick a shorter name")
            user = db.session.query(User).filter(User.id == int(request.form["id"])).all()[0]
            user.username = request.form["Username"]
            db.session.commit()
            return "all good!"