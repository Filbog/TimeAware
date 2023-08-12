from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from models import db, User, UserActivity, TrackActivity
from datetime import datetime, timedelta
from collections import defaultdict

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
        return render_template("login.html", user=current_user)


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
        statistics_data = calculate_statistics(activityName, periodInDays)
        # return jsonify(statistics_data)

    return render_template(
        "statistics.html", user=current_user, activities=current_user.activities
    )


def calculate_statistics(activity_names, period_in_days):
    today = datetime.now().date()
    start_date = today - timedelta(days=period_in_days)

    track_activities = (
        TrackActivity.query.join(UserActivity)
        .filter(
            UserActivity.name.in_(activity_names),
            TrackActivity.start_time >= start_date,
        )
        .all()
    )

    # Create a defaultdict to store the sum of durations for each day and activity
    daily_durations = defaultdict(lambda: defaultdict(int))

    # Calculate the total duration and sum of durations for each day and activity
    total_duration = 0
    for track_activity in track_activities:
        duration = track_activity.duration
        total_duration += duration

        # Get the date of the track_activity and add the duration to the corresponding day and activity
        activity_date = track_activity.start_time.date()
        activity_name = track_activity.user_activity.name
        daily_durations[str(activity_date)][
            activity_name
        ] += duration  # Convert the date to a string

    # Format the total_duration as before
    if total_duration > 3600:
        hours = int(total_duration / 3600)
        minutes = int((total_duration - hours * 3600) / 60)
        seconds = int(total_duration % 60)
        total_duration = f"{hours} hours, {int(minutes)} minutes and {seconds} seconds"
    elif total_duration > 60:
        total_duration = (
            f"{int(total_duration/60)} minutes and {total_duration % 60} seconds"
        )
    else:
        total_duration = f"{total_duration} seconds"

    # Return the calculated statistics data as a dictionary
    statistics_data = {
        "activity_names": activity_names,
        "period": period_in_days,
        "total_duration": total_duration,
        "daily_durations": daily_durations,
    }

    return statistics_data


@views.route("/get-statistics", methods=["GET"])
@login_required
def get_statistics():
    activity_names = request.args.get("activity").split(",")  # Split activity names
    period_in_days = int(request.args.get("period"))

    # Query the database to get the relevant statistics data
    statistics_data = calculate_statistics(activity_names, period_in_days)

    # Return the statistics data in JSON format
    return jsonify(statistics_data)


@views.route("/get-activity-options", methods=["GET"])
@login_required
def get_activity_options():
    # Fetch the available activity options from the database
    activity_options = [
        {"name": activity.name, "type": activity.type}
        for activity in UserActivity.query.all()
    ]
    # Return the activity options in JSON format
    return jsonify({"activity_options": activity_options})


@views.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    if request.method == "GET":
        return render_template(
            "dashboard.html", user=current_user, activities=current_user.activities
        )
    elif request.method == "POST":
        print(request.form)
        if "add-activity" in request.form:
            activity = request.form.get("add-activity").strip()
            type = request.form.get("type")
            print("Activity:", activity)
            print("Type:", type)
            activityExists = UserActivity.query.filter_by(name=activity).first()
            if len(activity) < 3:
                flash("Activity name must be at least 3 characters", category="error")
            elif activityExists:
                flash("Activity already exists", category="error")
            else:
                new_record = UserActivity(
                    name=activity, type=type, user_id=current_user.id
                )
                db.session.add(new_record)
                db.session.commit()
                activities = UserActivity.query.filter_by(user_id=current_user.id).all()
                print(activities)

                flash("Activity added!", category="success")
                return render_template(
                    "dashboard.html",
                    user=current_user,
                    activities=current_user.activities,
                )
        elif "browse-or-delete" in request.form:
            activity_id = request.form.get("browse-or-delete")
            # print(activity_id)
            if activity_id:
                activity = UserActivity.query.get(activity_id)
                # Retrieve all instances of the activity from the TrackActivity table
                track_activities = TrackActivity.query.filter_by(
                    user_activity_id=activity.id
                ).all()

                # Delete each instance of the activity from the TrackActivity table
                for track_activity in track_activities:
                    db.session.delete(track_activity)

                # Delete the activity from the UserActivity table
                db.session.delete(activity)
                db.session.commit()
                flash("Activity deleted successfully", category="success")
            else:
                flash("Please select an activity to delete", category="error")
    return render_template(
        "dashboard.html", user=current_user, activities=current_user.activities
    )


@views.route("/about")
def about():
    return render_template("about.html", user=current_user)
