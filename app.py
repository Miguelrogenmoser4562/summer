from flask import Flask, flash, redirect, render_template, render_template_string, request, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

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