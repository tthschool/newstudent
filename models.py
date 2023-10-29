from extensions import db
from flask import session 
from flask_login import UserMixin
from flask_wtf import FlaskForm 
from wtforms import StringField , PasswordField , SubmitField , DateField ,SelectField 
from wtforms.validators import input_required,  length , ValidationError , email


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(50), nullable=False)
    tasks = db.relationship('Task', backref='todo', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    todo_id = db.Column(db.Integer, db.ForeignKey('todo.id'), nullable=False)

class User_table(db.Model,UserMixin ):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20) , nullable = False , unique = True)
    password = db.Column(db.String(1000000) , nullable = False) 

class User_base(db.Model , UserMixin):
    id = db.Column(db.Integer , primary_key = True)
    user_name = db.Column(db.String(50) , nullable = False , unique  = True)
    password = db.Column(db.String(100000) , nullable  = False)
    student = db.relationship('Student' , backref='user_base'  ,uselist  = False)
    is_student = db.Column(db.Boolean  , default = True)
    is_admin = db.Column(db.Boolean  , default = False )

class Student(db.Model):
    id = db.Column(db.Integer , primary_key = True )
    Name = db.Column(db.String , nullable = False)
    Date_of_birth = db.Column(db.Date , nullable = False)
    age  = db.Column(db.Integer , nullable = False)
    Gender = db.Column(db.String , nullable = False)
    Nationality = db.Column(db.String , nullable = False)
    Address = db.Column(db.String , nullable = False)
    Email = db.Column(db.String)
    Phone_number= db.Column(db.String )
    Class = db.Column(db.String , nullable = False)
    Student_activity = db.Column(db.String)
    User_id = db.Column(db.Integer , db.ForeignKey('user_base.id') , nullable = False)

class add_student(FlaskForm):
    name = StringField(validators=[input_required()]  , render_kw={"placeholder":"student name"})
    date_of_birth = DateField( validators=[input_required()] , render_kw = {"placeholder":"date of birth"})
    age = StringField(validators=[input_required()] ,render_kw={"placeholder" : "age"} )
    gender_choice  =[('male' , 'male'),('female' ,'female'),('secret' ,'secret')]
    gender = SelectField('Gender' , choices=gender_choice ,validators=[input_required()])
    nationnality = StringField(validators=[input_required()] , render_kw={"placeholder" : "nationality"})
    address = StringField(validators=[input_required()] ,render_kw={"placeholder" : "address"})
    email = StringField(validators=[input_required() , email()] , render_kw={"placeholder":"email"})
    phone_number = StringField(validators=[input_required()] , render_kw={"placeholder" :"phone number"})
    Class = StringField(validators=[input_required()] , render_kw={"placeholder" :" Class"})
    Student_activity = StringField(render_kw={"placeholder" :"student activity"})
    user_name = StringField(validators=[input_required()] , render_kw={"placeholder" : "username"})
    password = PasswordField(validators=[input_required() , length(min = 4 , max = 100)] , render_kw={"placeholder":"password"} )
    submit = SubmitField("add")

class update_student(FlaskForm):
    name = StringField(validators=[input_required()]  , render_kw={"placeholder":"student name"})
    submit = SubmitField("update")
class Loginform(FlaskForm):
    username = StringField(validators=[input_required() , length(min=4 , max = 30)] , render_kw={"placeholder":"username"})
    password  = PasswordField(validators=[input_required() , length(min=4 , max = 20)] , render_kw={"placeholder":"password"})
    submit = SubmitField("login")
    

class registrationForm(FlaskForm):
    username = StringField(validators=[input_required() , length(min=4 , max = 30)] , render_kw={"placeholder":"username"})
    password  = PasswordField(validators=[input_required() , length(min=4 , max = 100)] , render_kw={"placeholder":"password"})
    checkpassword  = PasswordField(validators=[input_required() , length(min=4 , max = 100)] , render_kw={"placeholder":"check password"})
    submit = SubmitField("register")
    def validate_username(self , username):
        existing_username = User_table.query.filter_by(username=username.data).first()
        if existing_username:
            raise ValidationError('that username already exists')
    def check_password(self, password  , checkpassword):
        if password.data != checkpassword.data:
            raise ValidationError('password mismatch')
        

