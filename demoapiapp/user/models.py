from demoapiapp import db


class User(db.Model):

    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50),unique=True,nullable=False)
    password=db.Column(db.String(50),nullable=False)

    def __repr__(self):
        return f"username : {self.usename}"

