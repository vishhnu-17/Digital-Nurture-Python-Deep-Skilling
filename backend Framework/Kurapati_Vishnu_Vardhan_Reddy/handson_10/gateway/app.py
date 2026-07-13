from flask import Flask,request,jsonify
import requests
app=Flask(__name__)

@app.route("/api/courses",defaults={"path":""},methods=["GET","POST"])
@app.route("/api/courses/<path:path>",methods=["GET","POST","PUT","PATCH","DELETE"])
def course_proxy(path):
        url=f"http://127.0.0.1:5001/api/courses/{path}"
        response=requests.request(method=request.method,url=url,json=request.get_json(silent=True))
        return response.json(),response.status_code
    
@app.route("/api/students",defaults={"path":""},methods=["GET","POST"])
@app.route("/api/students/<path:path>",methods=["GET","PUT","POST","DELETE","PATCH"])
def student_proxy(path):
    url=f"http://127.0.0.1:5002/api/students/{path}"
    response=requests.request(method=request.method,url=url,json=request.get_json(silent=True)) 
    return response.json(),response.status_code   
if __name__=="__main__":
    app.run(port=5000,debug=True)
    
    
    