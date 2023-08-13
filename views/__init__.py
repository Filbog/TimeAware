from flask import Blueprint

views = Blueprint("views", __name__)

from . import home, save_tracked_activity_data, statistics, dashboard, about
