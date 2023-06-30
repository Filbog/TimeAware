from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    get_flashed_messages,
)
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from email_validator import validate_email, EmailNotValidError
from models import db, User

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("logged in successfully!", category="success")
                # this logs in the user in Flask. That 'remember=True' makes the server remember the session, so that the user isn't logged out every time they close the window
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password, try again", category="error")
        else:
            flash("email does not exist", category="error")
    return render_template("login.html", user=current_user)


@auth.route("/logout")
# this line makes sure that the user can access this page only if they're logged in
@login_required
def logout():
    logout_user()
    flash("logged out successfully", category="success")
    return redirect(url_for("auth.login"))


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

        user = User.query.filter_by(email=email).first()
        if user:
            flash("email already exists", category="error")
        elif len(firstName) < 3:
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
            new_user = User(
                email=email,
                firstName=firstName,
                password=generate_password_hash(password, method="pbkdf2"),
            )
            db.session.add(new_user)
            db.session.commit()
            # this line is temporary, in the future I'd like to send a confirmation email and only after clicking the link in there, the user is able to log in etc
            login_user(user, remember=True)
            flash("Account created!", category="success")
            return redirect(url_for("views.home"))
    return render_template("sign_up.html", user=current_user)
