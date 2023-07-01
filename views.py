from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from models import db, User

views = Blueprint("views", __name__)


@views.route("/")
def home():
    if current_user.is_authenticated:
        # # getting all the attributes of the current_user object
        # attributes = dir(current_user)
        # for attr in attributes:
        #     print(attr, getattr(current_user, attr))

        return render_template("index_logged.html", user=current_user)
    else:
        return render_template("index.html", user=current_user)


@views.route("/about")
def about():
    return render_template("about.html", user=current_user)


@views.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    if request.method == "GET":
        return render_template(
            "dashboard.html", user=current_user, activities=current_user.activities
        )
    elif request.method == "POST":
        activity = request.form.get("activity")
        type = request.form.get("type")
        print("Activity:", activity)
        print("Type:", type)

        # Rest of your code...
        flash("form submitted successfully", category="success")
        return render_template(
            "dashboard.html", user=current_user, activities=current_user.activities
        )
