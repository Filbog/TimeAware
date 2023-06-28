from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from datetime import timedelta

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    firstName = db.Column(db.String(50), nullable=False)
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

    def calculate_starting_time(self):
        return self.timestamp - timedelta(seconds=self.duration)


@db.event.listens_for(Activity, "before_insert", named=True)
def before_insert_listener(mapper, connection, target):
    target.starting_time = target.calculate_starting_time()
