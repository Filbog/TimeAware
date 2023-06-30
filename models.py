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
    # relations
    activities = db.relationship("Activity", back_populates="user")


class Activity(db.Model):
    __tablename__ = "activities"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())
    starting_time = db.Column(db.DateTime(timezone=True))
    # relations
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="activities")

    # method to calculate time of the start of the activity, so that I don't do two database insertions - 1st when starting the activity, 2nd when stopping
    def calculate_starting_time(self):
        return self.timestamp - timedelta(seconds=self.duration)


# event listener to add the starting time right before database insert
@db.event.listens_for(Activity, "before_insert", named=True)
def before_insert_listener(mapper, connection, target):
    target.starting_time = target.calculate_starting_time()
