from . import views
from flask import render_template
from flask_login import current_user


@views.route("/")
def home():
    if current_user.is_authenticated:
        # Your existing home route code
        return render_template(
            "tracker.html", user=current_user, activities=current_user.activities
        )
    else:
        return render_template("login.html", user=current_user)
