# Campus-Placement-Application

A Flask-based web application designed to streamline campus placement activities by enabling seamless interaction between students,companies and administrators.


In this system,
1. Students can register,view placement drives and apply for jobs.
2. Companies can create placement drives,manage postings and view applicants.
3. Administrators can approve companies,manage users,monitor activities and blacklist users if necessary.

For the backend, I used Flask as the web framework along with SQLAlchemy for database management.
SQLite was used as the database, while Bootstrap and Jinja2 were used for building responsive and dynamic user interfaces.

The application follows a modular architecture using Flask Blueprints and implements role-based authentication for secure access management.

The database consists of five main entities:
Student,Company,PlacementDrive,Application and Admin with proper one-to-many relationships between them.


Video Presentation
Drive Link
