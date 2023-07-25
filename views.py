from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from models import db, User, UserActivity, TrackActivity
from datetime import datetime, timedelta

views = Blueprint("views", __name__)


@views.route("/")
def home():
    if current_user.is_authenticated:
        # # getting all the attributes of the current_user object
        # attributes = dir(current_user)
        # for attr in attributes:
        #     print(attr, getattr(current_user, attr))

        return render_template(
            "tracker.html", user=current_user, activities=current_user.activities
        )
    else:
        return render_template("index.html", user=current_user)


@views.route("/save-tracked-activity-data", methods=["GET", "POST"])
def save_tracked_activity_data():
    if request.method == "POST":
        activity = request.form.get("activity")
        duration = request.form.get("duration")
        start_time_str = request.form.get("start_time")
        end_time_str = request.form.get("end_time")
        user_activity_id = request.form.get("user_activity_id")

        start_time = datetime.strptime(start_time_str, "%m/%d/%Y, %I:%M:%S %p")
        end_time = datetime.strptime(end_time_str, "%m/%d/%Y, %I:%M:%S %p")
        new_record = TrackActivity(
            duration=duration,
            end_time=end_time,
            start_time=start_time,
            user_activity_id=user_activity_id,
        )
        db.session.add(new_record)
        db.session.commit()
        flash("Tracking data saved successfully", category="success")
        return redirect(url_for("views.home"))


@views.route("/statistics", methods=["GET", "POST"])
@login_required
def statistics():
    if request.method == "POST":
        activityName = request.form.get("activity")
        # validators for activity
        activityExists = UserActivity.query.filter_by(name=activityName).first()
        activityType = UserActivity.query.filter_by(name=activityName).first().type
        print(activityType)

        if activityExists is None:
            flash("Invalid activity", category="error")
            return render_template(
                "statistics.html", user=current_user, activities=current_user.activities
            )

        periodInDays = request.form.get("periodInDays")

        # validators for periodInDays
        if (
            not periodInDays.isdigit()
            or int(periodInDays) > 365
            or int(periodInDays) < 1
        ):
            flash("Invalid time period", category="error")
            return render_template(
                "statistics.html", user=current_user, activities=current_user.activities
            )
        periodInDays = int(periodInDays)
        return redirect(
            url_for(
                "views.display_statistics",
                user=current_user,
                activity=activityName,
                period=periodInDays,
                activityType=activityType,
            )
        )

    return render_template(
        "statistics.html", user=current_user, activities=current_user.activities
    )


@views.route(
    "/display-statistics/<activity>/<int:period>/<activityType>", methods=["GET"]
)
@login_required
def display_statistics(activity, period, activityType):
    today = datetime.now().date()
    start_date = today - timedelta(days=period)
    activityName = activity
    track_activities = (
        TrackActivity.query.join(UserActivity)
        .filter(
            UserActivity.name == activity,
            TrackActivity.start_time >= start_date,
        )
        .all()
    )

    chart_data = {"labels": [], "data": []}
    total_duration = 0

    for activity in track_activities:
        date_str = activity.start_time.strftime("%Y-%m-%d")
        if date_str not in chart_data["labels"]:
            chart_data["labels"].append(date_str)
            chart_data["data"].append(activity.duration)
        else:
            index = chart_data["labels"].index(date_str)
            chart_data["data"][index] += activity.duration
        total_duration += activity.duration

    if total_duration > 3600:
        total_duration = f"{int(total_duration/3600)} hours, {int(total_duration/60)} minutes and {total_duration % 3600 } seconds"
    elif total_duration > 60:
        total_duration = (
            f"{int(total_duration/60)} minutes and {total_duration % 60 } seconds"
        )
    else:
        total_duration = f"{total_duration} seconds"

    return render_template(
        "display_statistics.html",
        activity=activity,
        **chart_data,
        user=current_user,
        activityName=activityName,
        activityType=activityType,
        total_duration=total_duration,
    )


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
        activityExists = UserActivity.query.filter_by(name=activity).first()
        if len(activity) < 3:
            flash("Activity name must be at least 3 characters", category="error")
        elif activityExists:
            flash("Activity already exists", category="error")
        else:
            new_record = UserActivity(name=activity, type=type, user_id=current_user.id)
            db.session.add(new_record)
            db.session.commit()
            activities = UserActivity.query.filter_by(user_id=current_user.id).all()
            print(activities)
            # Rest of your code...
            flash("Activity added!", category="success")
            return render_template(
                "dashboard.html", user=current_user, activities=current_user.activities
            )
    return render_template(
        "dashboard.html", user=current_user, activities=current_user.activities
    )


@views.route("/about")
def about():
    return render_template("about.html", user=current_user)
