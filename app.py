import json
from flask import Flask, flash, jsonify, render_template, request, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from models import *
from forms import * 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pokeapi'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "somekey"
toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

CURR_USER_KEY = "current_user"

#
# User stuff
#

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
        # print(g.user)

    else:
        g.user = None


def log_user_in(user):
    """puts active user in session"""
    session[CURR_USER_KEY] = user.id

def log_user_out():
    """takes user out of session"""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Processes signup or returns signup form"""

    form = NewUserForm()

    if form.validate_on_submit():
        # handle unique username error?
        username = form.username.data
        password = form.password.data
        user = User.signup(username, password)

        db.session.commit()
        log_user_in(user)
        return redirect("/")

    return render_template("/users/signup.html", form=form, user=g.user)

@app.route("/logout")
def logout():
    """removes current user"""
    if g.user:
        log_user_out()
        flash(f"Logged out user {g.user.username}")
        return redirect("/")
    
    else:
        flash("No user logged in")
        return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    """logs the user in"""

    form = LogUserIn()

    if form.validate_on_submit():
        user = User.authenticateUser(form.username.data, form.password.data)

        if user:
            log_user_in(user)
        else:
            flash("Incorrect credentials")
        return redirect("/")

    else:
        return render_template("/users/login.html", form=form, user=g.user)

@app.route("/user/<int:user_id>")
def user_profile(user_id):

    if not g.user:
        flash("Must be signed in to access")
        return render_template("/")
    
    # get list of all teams from db with user_id
    # iterate through teams
    # iterate through pokemon in teams
    # use jinja to setup name + sprite
    allTeams = PokemonTeam.query.filter(PokemonTeam.user_id==user_id).all()
    teamsArr = []
    numTeams = len(allTeams)
    i = 0
    while (i < numTeams):
        teamsArr.append([])
        teamsArr[i].append(allTeams[i].pokemon1)
        teamsArr[i].append(allTeams[i].pokemon1URL)
        teamsArr[i].append(allTeams[i].pokemon2)
        teamsArr[i].append(allTeams[i].pokemon2URL)
        teamsArr[i].append(allTeams[i].pokemon3)
        teamsArr[i].append(allTeams[i].pokemon3URL)
        teamsArr[i].append(allTeams[i].pokemon4)
        teamsArr[i].append(allTeams[i].pokemon4URL)
        teamsArr[i].append(allTeams[i].pokemon5)
        teamsArr[i].append(allTeams[i].pokemon5URL)
        teamsArr[i].append(allTeams[i].pokemon6)
        teamsArr[i].append(allTeams[i].pokemon6URL)
        teamsArr[i].append(allTeams[i].id)
        i += 1

    # print(teamsArr)

    return render_template("/users/profile.html", user=g.user, teams=teamsArr)

@app.route("/user/<int:user_id>/changepassword", methods=["GET", "POST"])
def change_password(user_id):
    """allows user to change password (encrypted)"""

    if not g.user:
        flash("Must be logged in ")
        return redirect("/")
    if g.user.id != user_id:
        flash("Must be logged in ")
        return redirect("/")
    
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if (not User.authenticateUser(g.user.username, form.oldPassword.data)):
            flash("Old password is incorrect")
            return redirect(f"/user/{user_id}/changepassword")
        if (not form.newPassword1.data == form.newPassword2.data):
            flash("New passwords must match")
            return redirect(f"/user/{user_id}/changepassword")
        
        User.changePassword(g.user.id, form.newPassword1.data)
        print("password changed")

        return redirect(f"/user/{user_id}")
    
    return render_template("/users/changepassword.html", form=form, user=g.user)

@app.route("/user/<int:user_id>/delete")
def delete_user(user_id):
    """deletes a user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/")

#
# Homepage
#

@app.route("/")
def temp_homepage():
    """Homepage with signin options"""
    return render_template("homepage.html", user=g.user)

#
# Pokemon team related stuff
#

@app.route("/teams/new", methods=["GET", "POST"])
def create_new_team():
    """Processing creating a new pokemon team"""
    
    if not g.user:
        flash("Must be logged in")
        return redirect("/")

    if request.method == "POST":
        response = request.get_json()
        # print(response)
        # this can probably just be a loop
        newTeam = PokemonTeam(
            pokemon1 = str(response[0][0]),
            pokemon1URL = str(response[0][1]),
            pokemon2 = str(response[1][0]),
            pokemon2URL = str(response[1][1]),
            pokemon3 = str(response[2][0]),
            pokemon3URL = str(response[2][1]),
            pokemon4 = str(response[3][0]),
            pokemon4URL = str(response[3][1]),
            pokemon5 = str(response[4][0]),
            pokemon5URL = str(response[4][1]),
            pokemon6 = str(response[5][0]),
            pokemon6URL = str(response[5][1]),
            user_id = g.user.id
        )
        db.session.add(newTeam)
        db.session.commit()

    return render_template("/teams/create-team.html", user=g.user)

@app.route("/teams/<int:team_id>/delete")
def delete_team(team_id):
    """deletes a user's team from the db"""
    team = PokemonTeam.query.get_or_404(team_id)
    db.session.delete(team)
    db.session.commit()
    return redirect(f"/user/{g.user.id}")