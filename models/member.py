from extensions import db
from flask_login import UserMixin


member_role = db.Table('member_role',
                       db.Column('member_id', db.Integer, db.ForeignKey('member.id')),
                       db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
                       )

member_retreat = db.Table('member_retreat',
                           db.Column('member_id', db.Integer, db.ForeignKey('member.id')),
                           db.Column('retreat_id', db.Integer, db.ForeignKey('retreat.id'))
                           )

class Member(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.Integer, unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    phone = db.Column(db.String(15), unique=True)
    whatsapp = db.Column(db.String(15))
    profession = db.Column(db.String(100))
    sex = db.Column(db.String(10))
    dob = db.Column(db.String(15))
    state = db.Column(db.String(100))
    website = db.Column(db.String(100))
    registration_date = db.Column(db.String(50))
    token = db.Column(db.String(10))
    role = db.relationship('Role', secondary=member_role, backref='members')
    retreat_participated = db.relationship('Retreat', secondary=member_retreat, backref='participants')

    def __repr__(self):
        return f'{self.name} -- {self.email}'


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(500))

    def __repr__(self):
        return f'{self.name}'


class Retreat(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    uuid=db.Column(db.Integer, unique=True)
    title = db.Column(db.String(100))
    subtitle = db.Column(db.String(200))
    date = db.Column(db.String(60))
    venue_line_1 = db.Column(db.String (50))
    venue_line_2 = db.Column(db.String (50))
    venue_line_3 = db.Column(db.String (50))
    city_country_pin = db.Column(db.String(50))
    landmark = db.Column(db.String(50))
    activity_1 = db.Column(db.String(50))
    activity_2 = db.Column(db.String(50))
    activity_3 = db.Column(db.String(50))
    activity_4 = db.Column(db.String(50))
    activity_5 = db.Column(db.String(50))
    activity_6 = db.Column(db.String(50))
    activity_7 = db.Column(db.String(50))
    activity_8 = db.Column(db.String(50))
    activity_9 = db.Column(db.String(50))
    prerequisites = db.Column(db.String(1000))
    stuffs_to_bring = db.Column(db.String(1000))
    accommodation = db.Column(db.String(1000))
    local_commutation = db.Column(db.String(1000))
    charges = db.Column(db.String(100))
    contact = db.Column(db.String(500))
    team = db.Column(db.String(1000))
    rules = db.Column(db.String(1000))
    total_interested = db.Column(db.Integer)
    total_registered = db.Column(db.Integer)
    amount_collection = db.Column(db.Integer)
    total_seats = db.Column(db.Integer)
    early_bird_seats = db.Column(db.Integer)
    suggestions = db.relationship('RetreatSuggestions', backref='retreat')
    feedbacks = db.relationship('RetreatFeedbacks', backref='retreat')

    def __repr__(self):
        return f'{self.title}'


class RetreatSuggestions(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    retreat_id = db.Column(db.Integer, db.ForeignKey('retreat.id'))
    member_id = db.Column(db.Integer)
    member_name = db.Column(db.String(100))
    suggestion = db.Column(db.String(200))

    def __repr__(self):
        return f'{self.member_name}--- Retreat_Id: {self.retreat_id}'


class RetreatFeedbacks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    retreat_id = db.Column(db.Integer, db.ForeignKey('retreat.id'))
    member_id = db.Column(db.Integer)
    member_name = db.Column(db.String(100))
    feedback = db.Column(db.String(200))

    def __repr__(self):
        return f'{self.member_name}--- Retreat_Id: {self.retreat_id}'