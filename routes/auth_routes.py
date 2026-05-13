from flask import Blueprint,render_template,request,redirect,session
from models import Student,Company, Admin,db
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
from flask import flash
import os

auth_bp=Blueprint("auth", __name__)
#Login function
@auth_bp.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        email=request.form["email"]
        password=request.form["password"]
        role=request.form["role"]

        if role=="student":
            user=Student.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):

               session.clear()   
               session["student_id"] = user.id
               return redirect("/student/dashboard")
            return redirect("/login")
        
        elif role=="company":
            user=Company.query.filter_by(company_name=email).first()
            if not user:
                  flash("Invalid company credentials", "danger")
                  return redirect("/login")
            if not check_password_hash(user.password, password):
               flash("Invalid password", "danger")
               return redirect("/login")
            if user.is_blacklisted:
               flash("Your company account has been blocked by admin. Please contact support.", "danger")
               return redirect("/login") 
            if not user.approved:
                flash("Your account is not approved yet. Please wait for admin approval.", "warning")
                return redirect("/login") 
            session.clear()
            session["company_id"] = user.id
            flash("Login successful!", "success")
            return redirect("/company/dashboard")

        elif role=="admin":
            admin=Admin.query.filter_by(username=email).first()

            if admin and check_password_hash(admin.password, password):
                session.clear()
                session["admin_id"]=admin.id
                return redirect("/admin/dashboard")

    return render_template("login.html")
#Student Register
@auth_bp.route("/student/register", methods=["GET","POST"])
def student_register():
    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])
        resume_path = None

        resume_file = request.files.get("resume")
        if resume_file and resume_file.filename:
            filename = secure_filename(resume_file.filename)
            if not filename.lower().endswith(".pdf"):
                flash("Only PDF files are allowed for resume upload.", "danger")
                return render_template("register_student.html")

            upload_dir = os.path.join("static", "resumes")
            os.makedirs(upload_dir, exist_ok=True)

            saved_path = os.path.join(upload_dir, filename)
            resume_file.save(saved_path)
            resume_path = f"static/resumes/{filename}"

        student = Student(
            name=name,
            email=email,
            password=password,
            resume=resume_path
        )

        db.session.add(student)
        db.session.commit()

        return redirect("/login")
    return render_template("register_student.html")
#Company Register
@auth_bp.route("/company/register", methods=["GET","POST"])
def company_register():

    if request.method == "POST":

        company = Company(
            company_name=request.form["company_name"],
            hr_contact=request.form["hr_contact"],
            website=request.form["website"],
            password=generate_password_hash(request.form["password"]),
            approved=False#since admin need to approve
        )

        db.session.add(company)
        db.session.commit()

        return redirect("/login")

    return render_template("register_company.html")
#Home page
@auth_bp.route("/")
def home():
    return render_template("home.html")
#Logout 
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
