# ********************************************FLASK API USING IN MEMORY DATA STRUCTURES****************************************

# ******************************************************IMPORTS****************************************************************
import os
from flask import Flask ,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# *********************************************************CONFIGURATIONS*********************************************************
basedir=os.path.abspath(os.path.dirname(__name__))  
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,"demoapi.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
Migrate(app,db)

# ***************************************************************ROUTES**********************************************************
from demoapiapp.course.models import Course,Student

# ***************************************************************/***************************************************************
@app.route('/',methods=['GET'])
def index():
    '''function will return the index page for the api application'''
    return "Welcome to flask api using sqlite database".upper()

# /courses
@app.route('/courses',methods=['GET'])
def get_courses():
    '''function will return list of courses if courses is added in the list else it will return message'''
    courses=Course.query.all()
    result=[{'id':course.id,'name':course.name,'price':course.price,'students':str(course.students)} for course in courses]
    return jsonify({"courses":result})

# ***************************************************************/course/<int:id>***************************************************************
@app.route('/course/<int:id>',methods=['GET'])
def get_course(id): 
    '''function will return course which matches the course id else it will return message'''
    course=Course.query.get(id)
    return jsonify({'id':course.id,'name':course.name,'price':course.price}) if course else jsonify({"message":"No course found!"}) 

# ***************************************************************/course/<int:id>/students***************************************************************
@app.route('/course/<int:id>/students',methods=['GET'])
def get_students(id):
    '''function will return the list of student for the specified course id else it will return message'''
    course=Course.query.get(id)
    students=[]
    for student in course.students:
        students.append({"id":student.id,"name":student.name,"age":student.age})
    return jsonify({"students":students}) if students else jsonify({"message":"No student added yet!"}) 

# ***************************************************************/course/<int:id>***************************************************************
@app.route('/students',methods=['GET'])
def get_all_students():
    students=Student.query.all()
    result=[]
    if students:
        for student in students:
            result.append({'id':student.id,'name':student.name,'age':student.age,'course':str(student.course)})
        return jsonify({"students":result})
    return jsonify({"messasge":"no student added yet!"})

# ***************************************************************/course/<int:id>***************************************************************
@app.route('/course/<string:name>',methods=['POST'])
def post_course(name):
    '''function will add the new course in the course list and returns the json object of newly added course'''
    request_data=request.get_json()
    course=Course(name=name,price=request_data['price'])
    db.session.add(course)
    db.session.commit()
    return jsonify({'id':course.id,'name':course.name,'price':course.price})


# ***************************************************************/course/<int:id>***************************************************************
@app.route('/course/<int:id>',methods=['PATCH'])
def update_course(id):
    '''function will update the information of the course specified'''
    request_data=request.get_json()
    course=Course.query.get(id)
    if course:
        course.name=request_data['name']
        course.price=request_data['price']
        db.session.commit()
        return jsonify ({'id':course.id,'name':course.name,'price':course.price})
    return jsonify({"message":"no course found!"})

# ***************************************************************/course/<int:id>***************************************************************
@app.route('/course/<int:id>',methods=['DELETE'])
def delete_course(id):
    '''function will delete the specified course'''
    course=Course.query.get(id)
    if course:
        db.session.delete(course)
        db.session.commit()
        return jsonify({'id':course.id,"name":course.name,'price':course.price})
    return jsonify({"message":"course not found"})

# ***************************************************************/course/<int:id>/student/<string:name>***************************************************************
@app.route('/course/<int:id>/student/<string:name>',methods=['POST'])
def post_student(id,name):
    '''function will add the new student into the specified course'''
    course=Course.query.get(id)
    if course:
        student=Student.query.filter_by(name=name).first()
        if student:
            student.course_id=id
            db.session.commit()
            return jsonify({'id':student.id,'name':student.name,'age':student.age})
        
        student=course.add_student(name)
        db.session.commit()
        return jsonify({'id':student.id,'name':student.name,'age':student.age})
        
    return jsonify({"message":"no course available"})

# ***************************************************************/course/<int:id>/student/<string:name>***************************************************************
@app.route('/course/<int:id>/student/<string:name>',methods=['PATCH'])
def update_student(id,name):
    '''function will update information of specified student'''
    course=Course.query.get(id)
    if course:
        for student in course.students:
            if student.name==name:
                student.name=request.json['name']
                db.session.commit()
                return jsonify({'id':student.id,'name':student.name,'age':student.age})
        return {"message":"no student found"}
    return jsonify({"message":"no course available"})

# ***************************************************************/course/<int:id>/student/<string:name>***************************************************************
@app.route('/course/<int:id>/student/<string:name>',methods=['DELETE'])
def delete_student(id,name):
    '''function will delete information of specified student'''
    course=Course.query.get(id)
    if course:
        if course.students:
            for student in course.students:
                if student.name==name:
                    delete_student=Student.query.filter_by(name=name).first()
                    course.students.remove(delete_student)
                    db.session.delete(delete_student)
                    db.session.commit()
                return jsonify({'id':student.id,'name':student.name,'age':student.age})
            return jsonify({"message":"no student found"})    
        return jsonify({"message":"no student added yet"})
    return jsonify({"message":"no course available"})

# ***************************************************************MAIN FUNCTION**********************************************************
