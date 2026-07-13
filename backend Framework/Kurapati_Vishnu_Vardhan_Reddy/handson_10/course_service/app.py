from flask import Flask
from config import Config
from extensions import db
from models import Department,Course
from flask import jsonify

app=Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
print(__name__)

with app.app_context():
    print(db.metadata.tables.keys())    
    db.create_all()


    
@app.get("/api/courses/<int:course_id>")
def get_course(course_id):
    course=Course.query.get(course_id)
    
    if not course:
        return jsonify({
            
            "message": "course not found"
        }),404   
    return jsonify(course.to_dict()),200     

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5001,debug=True)            