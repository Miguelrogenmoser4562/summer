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

    def __repr__(self):
        return '<User %r>' % self.username
    
@app.route("/start_data_1815")
def start_data():
    db.create_all()
    return redirect("/")

@app.route("/")
def home():
    if session.get("user_id") == None:
        return redirect("/login")
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if session.get("user_id") != None:
            return redirect("/")
        else:
            return render_template("login.html", error="")
    else:
        Username = request.form.get("Username")
        Password = request.form.get("Password")
        if Password == "" or Username == "":
            return render_template("login.html", error="Missing info", Password=Password, Username=Username)
        User_data = db.session.query(User.username, User.email, User.password, User.id).all()
        if len(User_data) == 0:
                return render_template("login.html", error="PLease Make an Account")
        for x in User_data:
            if x.username.replace(" ", "") != Username.replace(" ", "") and x.email.replace(" ", "") != Username.replace(" ", ""):
                return render_template("login.html", error="Wrong Username", Password=Password, Username=Username)
            elif x.password.replace(" ", "") != Password.replace(" ", ""):
                return render_template("login.html", error="Wrong Password", Password=Password, Username=Username)
            session['user_id'] = x.id
            return redirect("/")
            
        

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        if session.get("user_id") != None:
            return redirect("/")
        return render_template("register.html", error="none")
    else:
        Email = request.form.get("Email") 
        Password = request.form.get("Password")
        Username = request.form.get("Username")
        if Email == "" or Password == "" or Username == "":
            return render_template("register.html", error="Missing Info", Email=Email, Username=Username, Password=Password)
        if len(Username) >= 35:
            return render_template("register.html", error="Username is too Long", Email=Email, Username=Username, Password=Password)
        if db.session.query(User).filter(User.username == Username).count() >= 1:
            return render_template("register.html", error="Username Taken", Email=Email, Username=Username, Password=Password)
        if db.session.query(User).filter(User.email == Email).count() >= 1:
            return render_template("register.html", error="Email Already Used", Email=Email, Username=Username, Password=Password)
        person = User(email=Email, password=Password, username=Username)
        db.session.add(person)
        db.session.commit()
        session["user_id"] = db.session.query(User.id).filter(User.username == Username).first()[0]
        return redirect("/")
