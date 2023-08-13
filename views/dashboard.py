from . import views
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from models import db, User, UserActivity, TrackActivity
from datetime import datetime, timedelta
from collections import defaultdict


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
            activityExists = UserActivity.query.filter_by(
                name=activity, user_id=current_user.id
            ).first()
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
