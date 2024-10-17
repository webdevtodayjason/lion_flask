from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)  # Added is_admin field
    manager_email = db.Column(db.String(150), nullable=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=True)

    lion_entries = db.relationship('LIONEntry', backref='author', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LIONEntry(db.Model):
    entry_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    last_week_achievements = db.Column(db.Text, nullable=True)
    issues = db.Column(db.Text, nullable=True)
    opportunities = db.Column(db.Text, nullable=True)
    next_week_commitments = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class DailyLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    achievements = db.Column(db.Text, nullable=True)
    issues = db.Column(db.Text, nullable=True)
    opportunities = db.Column(db.Text, nullable=True)
    next_day_tasks = db.Column(db.Text, nullable=True)

    user = db.relationship('User', backref=db.backref('daily_logs', lazy=True))

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    recipients = db.Column(db.String(255))
    last_week = db.Column(db.Text, nullable=True)
    issues = db.Column(db.Text, nullable=True)
    opportunities = db.Column(db.Text, nullable=True)
    next_week = db.Column(db.Text, nullable=True)

    user = db.relationship('User', backref=db.backref('reports', lazy=True))

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    teams = db.relationship('Team', backref='company', lazy=True)

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    users = db.relationship('User', backref='team', lazy=True)
    manager_email = db.Column(db.String(150), nullable=True)
