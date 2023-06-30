from flask import Blueprint, render_template
from flask_login import login_required, current_user

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


@views.route("/stats")
@login_required
def stats():
    return render_template("stats.html", user=current_user)
