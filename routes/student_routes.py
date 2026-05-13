from flask import Blueprint, render_template, session, redirect,request
from models import PlacementDrive, Application, Student,db
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
from flask import flash
import os
student_bp = Blueprint("student", __name__)
#Student dashboard
@student_bp.route("/student/dashboard")
def student_dashboard():
    if "student_id" not in session:
        return redirect("/login")
    student = Student.query.get(session["student_id"])
    if not student :
        session.clear()
        flash("Your account no longer exists. Contact admin.", "danger")
        return redirect("/login")

    drives = PlacementDrive.query.filter_by(status="Approved").all()
    applications = Application.query.join(PlacementDrive).filter(
        Application.student_id == session["student_id"]
    ).all()

    applied_drive_ids = [app.drive_id for app in applications]
    return render_template("student_dashboard.html", 
                           drives=drives,
                           applications=applications,
                           applied_drive_ids=applied_drive_ids)
#Student Profile
@student_bp.route("/student/profile", methods=["GET","POST"])
def student_profile():
    student = Student.query.get(session["student_id"])
    if request.method == "POST":
        student.name = request.form["name"]
        student.email = request.form["email"]
        password = request.form["password"]
        if password:
            student.password = generate_password_hash(password)
        student.phone = request.form['phone']
        student.branch = request.form['branch']
        student.year = request.form['year']
        student.cgpa = request.form['cgpa']
        student.skills = request.form['skills']
        file = request.files.get("resume")
        if file and file.filename:
            upload_dir = os.path.join("static", "resumes")
            os.makedirs(upload_dir, exist_ok=True)

            filename = secure_filename(file.filename)
            if not filename.lower().endswith(".pdf"):
                flash("Only PDF files are allowed for resume upload.", "danger")
                return redirect("/student/profile")

            filepath = os.path.join(upload_dir, filename)
            file.save(filepath)
            # Store web-friendly path for template links.
            student.resume = f"static/resumes/{filename}"

        db.session.commit()
        flash("Profile updated successfully.", "success")

        return redirect("/student/profile")

    return render_template("student_profile.html", student=student)
#Apply Drive
@student_bp.route("/apply/<int:drive_id>")
def apply(drive_id):
    if "student_id" not in session:
        return redirect("/login")
    drive = PlacementDrive.query.get(drive_id)
    deadline_date = datetime.strptime(drive.deadline, "%Y-%m-%d").date()
    today = datetime.today().date()
    if deadline_date < today:
        flash("Application deadline has passed", "danger")
        return redirect("/student/dashboard")
    student_id = session["student_id"]
    student = Student.query.get(student_id)
    if student.is_blacklisted:
        flash("You are blacklisted and cannot apply for jobs", "danger")
        return redirect("/student/dashboard")
    existing = Application.query.filter_by(
        student_id=student_id,
        drive_id=drive_id
    ).first()
    if existing:
        flash("Already Applied", "warning")
        return redirect("/student/dashboard")

    application = Application(
        student_id=student_id,
        drive_id=drive_id,
        status="Applied"
    )

    db.session.add(application)
    db.session.commit()

    flash("Application submitted successfully", "success")

    return redirect("/student/dashboard")