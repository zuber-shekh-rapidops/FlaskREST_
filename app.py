# ********************************************FLASK API USING IN MEMORY DATA STRUCTURES****************************************

# ******************************************************IMPORTS****************************************************************
import os
from flask import Flask ,jsonify,request

# *********************************************************CONFIGURATIONS*********************************************************
basedir=os.path.abspath(os.path.dirname(__name__))  
app=Flask(__name__)

# ***************************************************************ROUTES**********************************************************
courses=[
    {
        "id":1,
        "name":"python a to z",
        "price":1200,
        "students":[
            {
                "name":"kabir"
            }
        ]
    }
]
# ***************************************************************/***************************************************************
@app.route('/',methods=['GET'])
def index():
    '''function will return the index page for the api application'''
    return "Welcome to flask api using in memory data structures".upper()

# /courses
@app.route('/courses',methods=['GET'])
def get_courses():
    '''function will return list of courses if courses is added in the list else it will return message'''
    return jsonify({"message":"No course added yet!"}) if courses == [] else jsonify({"courses":courses})

# ***************************************************************/course/<int:id>***************************************************************
@app.route('/course/<int:id>',methods=['GET'])
def get_course(id): 
    '''function will return course which matches the course id else it will return message'''
    course=[c for c in courses if c['id']==id]
    return jsonify({"message":"No course found!"}) if course == [] else jsonify(course[0])

# ***************************************************************/course/<int:id>/students***************************************************************
@app.route('/course/<int:id>/students',methods=['GET'])
def get_students(id):
    '''function will return the list of student for the specified course id else it will return message'''
    students=[c['students'] for c in courses if c['id']==id ]
    return jsonify({"message":"No student added yet!"}) if students == [] else jsonify(students[0])

# ***************************************************************/course/<int:id>***************************************************************
@app.route('/course/<int:id>',methods=['POST'])
def post_course(id):
    '''function will add the new course in the course list and returns the json object of newly added course'''
    request_data=request.get_json()
    new_course={
        "id":id,
        "name":request_data['name'],
        "price":request_data['price'],
        "students":[]
    }
    courses.append(new_course)
    return jsonify(new_course)

# ***************************************************************/course/<int:id>***************************************************************
@app.route('/course/<int:id>',methods=['PATCH'])
def update_course(id):
    '''function will update the information of the course specified'''
    request_data=request.get_json()
    course=[c for c in courses if c['id']==id]
    if course!=[]:
        course[0]['name']=request_data['name']
        course[0]['price']=request_data['price']
        return jsonify ({"message":"course updated!"})
    return jsonify({"message":"no course found!"})

# ***************************************************************/course/<int:id>***************************************************************
@app.route('/course/<int:id>',methods=['PUT'])
def update_course_with_put(id):
    '''function will update the information of the course specified'''
    request_data=request.get_json()
    course=[c for c in courses if c['id']==id]
    if course!=[]:
        course[0]['name']=request_data['name']
        return jsonify ({"message":"course updated!"})
    return jsonify({"message":"no course found!"})

# ***************************************************************/course/<int:id>***************************************************************
@app.route('/course/<int:id>',methods=['DELETE'])
def delete_course(id):
    '''function will delete the specified course'''
    course=[c for c in courses if c['id']==id]
    if course:
        courses.remove(course[0])   
        return jsonify({"message":"course deleted!"})
    return jsonify({"message":"no course found!"})

# ***************************************************************/course/<int:id>/student/<string:name>***************************************************************
@app.route('/course/<int:id>/student/<string:name>',methods=['GET'])
def get_student(id,name):
    '''function will return json object for student if avaliable in the list else returns the message'''
    course=[c for c in courses if c['id']==id]
    if course!=[]:
        student=[s for s in course[0]['students'] if s['name']==name]
    return jsonify(student[0]) if student else jsonify({"message":"no student available"})

# ***************************************************************/course/<int:id>/student/<string:name>***************************************************************
@app.route('/course/<int:id>/student/<string:name>',methods=['POST'])
def post_student(id,name):
    '''function will add the new student into the specified course'''
    course=[c for c in courses if c['id']==id]
    if course!=[]:
        new_student={"name":name}
        course[0]['students'].append(new_student)
    return jsonify(new_student) if courses else jsonify({"message":"no course available"})

# ***************************************************************/course/<int:id>/student/<string:name>***************************************************************
@app.route('/course/<int:id>/student/<string:name>',methods=['PATCH'])
def update_student(id,name):
    '''function will update information of specified student'''
    course=[c for c in courses if c['id']==id]
    if course!=[]:
        student=[s for s in course[0]['students'] if s['name']==name]
        if student:
            request_data=request.get_json()
            student[0]['name']=request_data['name']
            return {"message":"student updated!"}
        return {"message":"no student found"}
    return jsonify({"message":"no course available"})

# ***************************************************************/course/<int:id>/student/<string:name>***************************************************************
@app.route('/course/<int:id>/student/<string:name>',methods=['DELETE'])
def delete_student(id,name):
    '''function will delete information of specified student'''
    course=[c for c in courses if c['id']==id]
    if course!=[]:
        student=[s for s in course[0]['students'] if s['name']==name]
        if student:
            course[0]['students'].remove(student[0])
            return {"message":"student deleted!"}
        return {"message":"no student found"}
    return jsonify({"message":"no course available"})

# ***************************************************************MAIN FUNCTION**********************************************************
if __name__ == "__main__":
    app.run(debug=True)