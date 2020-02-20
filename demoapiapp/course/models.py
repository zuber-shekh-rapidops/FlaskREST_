from demoapiapp import db


class Course(db.Model):

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=False)
    price=db.Column(db.String(50),nullable=False)
    students=db.relationship('Student',backref='course',lazy=True)

    def __repr__(self):
        return f"name : {self.name} | price : {self.price}"
    
    def add_student(self,name):
        student=Student(name=name,course_id=self.id)
        db.session.add(student)
        db.session.commit()
        return student

class Student(db.Model):

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=False)
    age=db.Column(db.Integer,nullable=False,default=18)
    course_id=db.Column(db.Integer,db.ForeignKey('course.id'))

    def __repr__(self):
        return f"name : {self.name} | age : {self.age}"