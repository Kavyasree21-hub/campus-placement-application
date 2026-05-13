from flask import Blueprint, render_template, redirect, session, request
from models import Student, Company, PlacementDrive, Application,db
#from extensions import db

admin_bp = Blueprint("admin", __name__)
#Admin dashboard
@admin_bp.route("/admin/dashboard")
def admin_dashboard():

    if "admin_id" not in session:
        return redirect("/login")

    return render_template(
        "admin_dashboard.html",
        students=Student.query.count(),
        companies=Company.query.count(),
        drives=PlacementDrive.query.count(),
        applications=Application.query.count(),
        pending_companies=Company.query.filter_by(approved=False).all(),
        pending_drives=PlacementDrive.query.filter_by(status="Pending").all()
    )


# View pages
@admin_bp.route("/admin/students")
def view_students():

    search = request.args.get("search")
    query = Student.query
    if search:
        query = query.filter(
            (Student.name.ilike(f"%{search}%"))|
            (Student.email.ilike(f"%{search}%")) |
            (Student.id.like(f"%{search}%"))
        )
    students = query.all()
    return render_template("admin_students.html", students=students)

@admin_bp.route("/admin/companies")
def view_companies():
    search = request.args.get("search")
    if search:
        companies = Company.query.filter(
            (Company.company_name.ilike(f"%{search}%")) |
            (Company.id.like(f"%{search}%"))
        ).all()
    else:
        companies = Company.query.all()
    return render_template("admin_companies.html", companies=companies)

@admin_bp.route("/admin/drives")
def view_drives():
    drives = PlacementDrive.query.filter_by(is_active=True).all()
    return render_template("admin_drives.html", drives=drives)

#Search student

@admin_bp.route("/search_student", methods=["POST"])
def search_student():
    keyword = request.form["keyword"]
    students_list = Student.query.filter(
        Student.name.contains(keyword)
    ).all()

    return render_template(
        "admin_dashboard.html",
        students_list=students_list,
        students=Student.query.count(),
        companies=Company.query.count(),
        drives=PlacementDrive.query.count(),
        applications=Application.query.count(),
        pending_companies=Company.query.filter_by(approved=False).all(),
        #pending_drives=PlacementDrive.query.filter_by(status="Pending").all()
    )

#Approve Company
@admin_bp.route("/approve_company/<int:id>")
def approve_company(id):
    c = Company.query.get(id)
    c.approved = True
    db.session.commit()
    return redirect("/admin/dashboard")
#Reject Company
@admin_bp.route("/reject_company/<int:id>")
def reject_company(id):
    company = Company.query.get(id)
    db.session.delete(company)
    db.session.commit()
    return redirect("/admin/dashboard")
#Approve Drive
@admin_bp.route("/approve_drive/<int:id>")
def approve_drive(id):
    drive = PlacementDrive.query.get(id)
    drive.status = "Approved"
    db.session.commit()
    return redirect("/admin/dashboard")
#Blacklist Student
@admin_bp.route("/blacklist_student/<int:id>")
def blacklist_student(id):
    student = Student.query.get(id)
    student.is_blacklisted = True
    db.session.commit()
    return redirect("/admin/students")
#Blacklist Company
@admin_bp.route("/blacklist_company/<int:id>")
def blacklist_company(id):
    company = Company.query.get(id)
    company.is_blacklisted = True
    db.session.commit()
    return redirect("/admin/companies")
#Delete Drive
@admin_bp.route("/delete_drive/<int:id>")
def delete_drive(id):
    if "admin_id" not in session:
        return redirect("/login")
    
    drive = PlacementDrive.query.get(id)
    if drive:
        db.session.delete(drive)
        db.session.commit()
    return redirect("/admin/drives")
#Delete Student
@admin_bp.route("/delete_student/<int:id>")
def delete_student(id):
    s = Student.query.get(id)
    if s:
        db.session.delete(s) 
        db.session.commit()
    return redirect("/admin/students")
