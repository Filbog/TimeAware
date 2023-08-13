from . import views
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from models import db, User, UserActivity, TrackActivity
from datetime import datetime, timedelta
from collections import defaultdict


@views.route("/about")
def about():
    return render_template("about.html", user=current_user)
