from . import views
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from models import db, User, UserActivity, TrackActivity
from datetime import datetime, timedelta
from collections import defaultdict


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
            UserActivity.user_id == current_user.id,
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
        for activity in UserActivity.query.filter_by(user_id=current_user.id).all()
    ]
    # Return the activity options in JSON format
    return jsonify({"activity_options": activity_options})
