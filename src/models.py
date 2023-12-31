from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

# timedelta converts my duration, which is in seconds, to a datetime format
from datetime import timedelta
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    firstName = db.Column(db.String(50), nullable=False)
    # relation to UserActivity (one-to-many)
    activities = db.relationship("UserActivity", back_populates="user")


class UserActivity(db.Model):
    __tablename__ = "user_activities"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    # relation to User (many-to-one)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="activities")
    # relation to TrackActivity (one-to-many)
    track_activities = db.relationship("TrackActivity", back_populates="user_activity")


class TrackActivity(db.Model):
    __tablename__ = "track_activities"
    id = db.Column(db.Integer, primary_key=True)
    duration = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.DateTime(timezone=True))
    end_time = db.Column(db.DateTime(timezone=True))
    # relation to UserActivity (many-to-one)
    user_activity_id = db.Column(
        db.Integer, db.ForeignKey("user_activities.id"), nullable=False
    )
    user_activity = db.relationship("UserActivity", back_populates="track_activities")
