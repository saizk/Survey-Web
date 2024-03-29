from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user

from . import db, bcrypt
from . import model

bp = Blueprint("auth", __name__)

@bp.route("/signup")
def signup():
    return render_template("auth/signup.html", current_user=current_user)

@bp.route("/signup", methods=["POST"])
def signup_post():
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")
    # Check that passwords are equal
    if password != request.form.get("password_repeat"):
        flash("Passwords do not match!")
        return redirect(url_for("auth.signup"))
    # Check if the email is already at the database
    user = model.User.query.filter_by(email=email).first()
    if user:
        flash("Email address already exists")
        return redirect(url_for("auth.signup"))
    # Create new user with its pwd hash
    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = model.User(email=email, name=username, password=password_hash)
    # Add user to the database
    db.session.add(new_user)
    db.session.commit()
    # Successfull login
    flash("You've successfully signed up!")
    return redirect(url_for("auth.login"))

@bp.route("/login")
def login():
    return render_template("auth/login.html", current_user=current_user)

@bp.route('/login', methods=['POST'])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = model.User.query.filter_by(email=email).first()
    
    if not user or not bcrypt.check_password_hash(user.password, password):
        flash(" Check your login credentials")
        return redirect(url_for("auth.login"))
    
    # The user has the right credentials
    login_user(user, remember=remember)
    
    return redirect(url_for('main.index', name=current_user.name))

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template("main/index.html")