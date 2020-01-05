from app import db
from datetime import datetime


class User(db.Model):
    uuid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    fname = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(35), nullable=False)
    is_verified = db.Column(db.Boolean(), default=False)
    profile_pic = db.Column(db.Text(), default="default.jpg")
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    events = db.relationship("Event", backref="organizer", lazy=True)

    def __repr__(self):
        return f"User({self.uuid}, {self.fname}, {self.surname}, {self.email})"


class Event(db.Model):
    uuid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    date_posted = db.Column(db.String(50), nullable=False, default=datetime.now().isoformat())
    description = db.Column(db.Text)
    user_uuid = db.Column(db.Integer, db.ForeignKey("user.uuid"), nullable=False)

    def __repr__(self):
        return f"Event({self.uuid}, {self.title}, {self.description}, oranizer id={self.user_uuid})"
