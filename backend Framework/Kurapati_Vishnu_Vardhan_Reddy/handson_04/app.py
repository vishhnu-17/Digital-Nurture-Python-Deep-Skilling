from flask import Flask
from config import Config
from courses.routes import courses_bp
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    print(app.config['SECRET_KEY'])
    app.register_blueprint(courses_bp)
    return app

app= create_app()
# @app.errorhandler(404)
# def not_found(error):
#     return jsonify({"status":"error","message":"resource not found"}),404

@app.errorhandler(500)
def internal_server(error):
    return jsonify({"status":"error","message":"internal server"}),500
if __name__=="__main__":
    app.run(debug=True)