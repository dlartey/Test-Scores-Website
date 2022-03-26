from app import db
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from datetime import datetime 
from werkzeug.security import generate_password_hash, check_password_hash

enrollment = db.Table('enrollment',
    db.Column('studentID', db.Integer, db.ForeignKey('student.id')),
    db.Column('moduleID', db.Integer, db.ForeignKey('module.id'))
)

class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True)
    firstName = db.Column(db.String(30))
    lastName = db.Column(db.String(30))
    password_hash = db.Column(db.String(128))
    studentScores = db.relationship('Scores', backref='ss', lazy='dynamic')  
    modules = db.relationship('Module',secondary=enrollment)


    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)    

class Module(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(30))
    students = db.relationship('Student',secondary=enrollment, overlaps="modules")
    moduleScores = db.relationship('Scores', backref='ms', lazy='dynamic')

class Scores(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    s_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    m_id = db.Column(db.Integer, db.ForeignKey('module.id'))
    score = db.Column(db.Integer)
    date =  db.Column (db.DateTime, default=datetime.utcnow)


# Each Student can take many modules
# Each module has many students
