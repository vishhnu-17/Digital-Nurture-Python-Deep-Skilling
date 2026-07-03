from extensions import db,migrate
from flask import Flask
from config import Config
def create_app():
    app=Flask(__name__)
    app.config.from_object(Config) # This means Flask reads every uppercase variable from the Config class.
    db.init_app(app)
    migrate.init_app(app,db)
    from courses.routes import courses_bp
    from courses import models
    app.register_blueprint(courses_bp)
    return app
app=create_app()
if __name__=="__main__":
    app.run(debug=True)
