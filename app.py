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
    points = db.Column(db.Integer, default=0)
    admin = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<User %r>' % self.username

class Games(db.Model):
    local = db.Column(db.String())
    visitor = db.Column(db.String())
    result = db.Column(db.String())
    id = db.Column(db.Integer, primary_key=True)
    round = db.Column(db.Integer)

    def __repr__(self):
        return '<Game %r>' % self.id
    
@app.route("/start_data_1815")
def start_data():
    db.create_all()
    return redirect("/")

@app.route("/first_admin")
def first_admin():
    if session.get("user_id") == None:
        return redirect("/login")
    if db.session.query(User).filter(User.admin == 1).count() > 0:
        return "MORE THAN ONE ADMIN"
    user = db.session.query(User).filter(User.id == session["user_id"]).all()
    user[0].admin = 1
    db.session.commit()
    return redirect("/")

@app.route("/")
def home():
    if request.method == "GET":
        if session.get("user_id") == None:
            return redirect("/login")
        Username = db.session.query(User.username).filter(User.id == session["user_id"]).all()[0].username

        # Scoreboard
        users = db.session.query(User.username, User.points).order_by(User.points).limit(10).all()
        users_needed = db.session.query(User).limit(10).count()
        admin = db.session.query(User).filter(User.id == session["user_id"]).all()[0].admin
        return render_template("home.html", users=users, count=users_needed, Username=Username, admin=admin)


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
                return render_template("login.html", error="Please Make an Account")
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
@app.route("/scoreboard", methods=["POST"])
def scoreboard():
    Users = db.session.query(User).order_by(User.points).all()
    User_count = db.session.query(User).count()
    return render_template("scoreboard.html", users=Users, count=User_count)