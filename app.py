from flask import Flask
from models import db,Admin
from werkzeug.security import generate_password_hash, check_password_hash

from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.student_routes import student_bp
from routes.company_routes import company_bp

app=Flask(__name__)

app.config['SECRET_KEY'] = 'secret123'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'

db.init_app(app)

#Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(student_bp)
app.register_blueprint(company_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        
        if not Admin.query.first():
            admin = Admin(username="admin@ppa.in",password=generate_password_hash("admin123"))
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True)