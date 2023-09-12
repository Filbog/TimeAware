from . import views
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from models import db, User, UserActivity, TrackActivity
from datetime import datetime, timedelta
from collections import defaultdict


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
