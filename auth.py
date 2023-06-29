from flask import Blueprint, render_template, request, flash
from email_validator import validate_email, EmailNotValidError

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html", temp="E BEBEBEBEBEB")


@auth.route("/login", methods=["POST"])
def login_post():
    return render_template("login.html", temp="E BEBEBEBEBEB")


@auth.route("/logout")
def logout():
    return "<h1>logout</h1>"


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    ### POST ###
    if request.method == "POST":
        email = request.form.get("email")
        firstName = request.form.get("name")
        password = request.form.get("password")
        password2 = request.form.get("password2")
        # authentication. For email, I'm using email_validator library
        try:
            isValid = validate_email(email, check_deliverability=True)
            email = isValid.normalized
        except EmailNotValidError as e:
            flash(e, category="error")
            return render_template("sign_up.html")
        if len(firstName) < 3:
            flash("Name must be greater than 2 characters.", category="error")
        elif len(firstName) > 30:
            flash("Name length is maximum 30 characters", category="error")
        elif len(password) < 5:
            flash("Your password must be at least 6 characters.", category="error")
        elif len(password) > 30:
            flash("password must be maximum 30 characters", category="error")
        elif password != password2:
            flash("Passwords don't match.", category="error")
        else:
            # add user to database
            flash("Account created!", category="success")
    return render_template("sign_up.html")
