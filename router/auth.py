from flask import Flask , Blueprint ,render_template , request , url_for , redirect ,session , flash
from flask_login import login_manager , UserMixin , login_required   , login_user , current_user , logout_user 
from models import Loginform   , registrationForm , User_base , Student
from extensions import db  , bcrypt
auth_bl = Blueprint('auth' , __name__)



@auth_bl.route('/login' , methods=['GET', 'POST'])
def login():
    form = Loginform()
    if form.validate_on_submit():
        username = form.username.data
        user = User_base.query.filter_by(user_name=username).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if user.is_admin == True:
                login_user(user)
                session['user'] = user.id
                current_user = user
                return redirect(url_for('main.home'))
            elif (user.is_admin == False) and (user.is_student == True):
                login_user(user)
                session['user'] = user.id
                current_user = user
                student = Student.query.filter_by(User_id = user.id).first()
                return redirect(url_for('main.student_detail' ,id = student.id))

    return render_template('login.html', form=form)

@auth_bl.route('/regis' , methods=['GET', 'POST'])
def regis():
    
    form = registrationForm()
    existing_user = User_base.query.all()
    if form.validate_on_submit() and not existing_user :
        password = form.password.data
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User_base(user_name = form.username.data, password = hashed_password , is_student  = False , is_admin = True)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))
    else:
        flash("permission denied" , "message")
        
    return render_template('regis.html', form=form)

@auth_bl.route('/logout' , methods = ['POST' , 'GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))



