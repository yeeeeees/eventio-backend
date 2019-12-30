from app import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    fname = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(35), nullable=False)
    is_verified = db.Column(db.Boolean(), default=False)
    profile_pic = db.Column(db.Text(), default="default.jpg")
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    events = db.relationship("Event", backref="organizer", lazy=True)

    def __repr__(self):
        print(f"User({self.id}, {self.name}, {self.surname}, {self.email}")


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    date_posted = db.Column(db.String(50), nullable=False, default=datetime.now().isoformat())
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
