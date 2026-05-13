from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    resume = db.Column(db.String(200))
    password = db.Column(db.String(100))
    phone = db.Column(db.String(15),nullable=True) 
    branch = db.Column(db.String(50)) 
    year = db.Column(db.String(10)) 
    cgpa = db.Column(db.Float) 
    skills = db.Column(db.String(200))

    applications = db.relationship('Application', backref='student',cascade="all, delete",
    passive_deletes=True)
    is_blacklisted = db.Column(db.Boolean, default=False)
    

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100),unique=True)
    hr_contact = db.Column(db.String(100))
    website = db.Column(db.String(100))
    password = db.Column(db.String(100))
    approved = db.Column(db.Boolean, default=False)
    company_email = db.Column(db.String(100),unique=True)
    
    drives = db.relationship('PlacementDrive', backref='company', lazy=True)
    is_blacklisted = db.Column(db.Boolean, default=False)

class PlacementDrive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer,db.ForeignKey('company.id')  )
    job_title = db.Column(db.String(100))
    description = db.Column(db.Text)
    eligibility = db.Column(db.String(200))
    deadline = db.Column(db.String(50))
    status = db.Column(db.String(50))
    is_active=db.Column(db.Boolean,default=True)
    created_date = db.Column(db.DateTime,default=datetime.now)
    applications = db.relationship('Application', 
                                   backref='drive',
                                   cascade="all, delete", 
                                   passive_deletes=True)
    

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer,db.ForeignKey('student.id',ondelete="CASCADE"))
    drive_id = db.Column(db.Integer,db.ForeignKey('placement_drive.id',ondelete="CASCADE"))
    status = db.Column(db.String(50))
    
    application_date = db.Column(db.DateTime, default=datetime.now)