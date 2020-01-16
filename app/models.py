from app import db
from datetime import datetime


def datetime_now_iso_format():
    return datetime.now().isoformat()[:-10]


class User(db.Model):
    uuid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    fname = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(35), nullable=False)
    is_verified = db.Column(db.Boolean(), default=False)
    profile_pic = db.Column(db.Text(), default="default.jpg")
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    created_events = db.relationship("Event", backref="organizer", lazy=True)
    joined_events = db.relationship("Event", secondary="joins", backref="joined_users")

    def __repr__(self):
        return f"User({self.uuid}, {self.fname}, {self.surname}, {self.email})"


class Event(db.Model):
    uuid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    date_posted = db.Column(db.String(25), nullable=False, default=datetime_now_iso_format)
    location = db.Column(db.String(100))
    description = db.Column(db.Text)
    organizer_uuid = db.Column(db.Integer, db.ForeignKey("user.uuid"), nullable=False)

    def __repr__(self):
        return f"Event({self.uuid}, {self.title}, {self.description}, oranizer id={self.organizer_uuid})"


joins = db.Table("joins",
                 db.Column("user_uuid", db.Integer, db.ForeignKey("user.uuid")),
                 db.Column("event_uuid", db.Integer, db.ForeignKey("event.uuid"))
                 )
