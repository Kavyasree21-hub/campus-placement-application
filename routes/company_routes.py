from flask import Blueprint, render_template, session, redirect,request
from models import PlacementDrive,db,Application,Company,Student
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
company_bp=Blueprint("company", __name__)
#Company Dashboard
@company_bp.route("/company/dashboard")
def company_dashboard():

    if "company_id" not in session:
        return redirect("/login")

    drives=PlacementDrive.query.filter_by(company_id=session["company_id"]).all()

    return render_template("company_dashboard.html", drives=drives)
#Apply Drive
@company_bp.route("/view_applications/<int:drive_id>")
def view_applications(drive_id):

    applications = Application.query.join(Student).filter(
        Application.drive_id==drive_id,
        Student.is_blacklisted==False
    ).all()

    return render_template(
        "view_applications.html",
        applications=applications
    )
#Creta Drive
@company_bp.route("/create_drive", methods=["GET","POST"])
def create_drive():
    if request.method == "POST":
        errors = {}
        title = request.form["title"]
        description = request.form["description"]
        eligibility = request.form["eligibility"]
        deadline_str = request.form["deadline"]

        deadline_date = datetime.strptime(deadline_str, "%Y-%m-%d").date()
        today = datetime.today().date()

        if deadline_date < today:
            errors["deadline"] = "Deadline cannot be in the past"
        if not title:
            errors["title"] = "Job title is required"
        if errors:
            return render_template(
                "create_drive.html",
                form_data=request.form,
                errors=errors
            )
        drive = PlacementDrive(
            company_id=session["company_id"],
            job_title=title,
            description=description,
            eligibility=eligibility,
            deadline=deadline_str,
            status="Pending"
        )
        db.session.add(drive)
        db.session.commit()
        return redirect("/company/dashboard")
    return render_template("create_drive.html", form_data=None, errors={})
#Edit Drive
@company_bp.route("/edit_drive/<int:id>", methods=["GET", "POST"])
def edit_drive(id):
    drive = PlacementDrive.query.get(id)
    if drive.company_id != session["company_id"]:
        return "Unauthorized", 403
    if request.method == "POST":
        drive.job_title = request.form["title"]
        drive.description = request.form["description"]
        drive.eligibility = request.form["eligibility"]
        drive.deadline = request.form["deadline"]
        db.session.commit()

        return redirect("/company/dashboard")
    return render_template("edit_drive.html", drive=drive)
#Delete drive
@company_bp.route("/company/delete_drive/<int:id>")
def company_delete_drive(id):
    if "company_id" not in session:
        return redirect("/login")
    drive = PlacementDrive.query.get(id)
    if drive.company_id != session["company_id"]:
        return "Unauthorized", 403
    db.session.delete(drive)
    drive.is_active = False
    db.session.commit()
    return redirect("/company/dashboard")
#Company Profile
@company_bp.route("/company/profile", methods=["GET", "POST"])
def company_profile():

    if "company_id" not in session:
        return redirect("/login")

    company = Company.query.get(session["company_id"])

    if request.method == "POST":
        company.company_name = request.form["company_name"]
        company.hr_contact = request.form["hr_contact"]
        company.website = request.form["website"]

        password = request.form["password"]
        if password:
            company.password = generate_password_hash(password)

        db.session.commit()

        return redirect("/company/profile")

    return render_template("company_profile.html", company=company)
#Update Application Status
@company_bp.route("/update_status/<int:id>/<status>")
def update_status(id,status):

    application = Application.query.get(id)

    application.status = status

    db.session.commit()

    return redirect("/company/dashboard")
   