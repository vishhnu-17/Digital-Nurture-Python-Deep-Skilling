from config import Config
from courses.routes import courses_bp, students_bp, enrollments_bp
from flask import Flask, jsonify
from extensions import db, migrate

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    from courses.models import Department, Course, Student, Enrollment

    migrate.init_app(app, db)

    app.register_blueprint(courses_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(enrollments_bp)

    return app



if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)