from flask import Flask , Blueprint , render_template , request , session , url_for ,redirect  , flash 
from flask_login import login_required ,current_user
from extensions import db
from models import Todo , Task , Student , User_base , update_student
from models import add_student
from extensions import bcrypt 
main_bl = Blueprint('main', __name__)





@main_bl.route('/' , methods = ["POST","GET"])
@login_required
def home():
    print(current_user.is_student)
    exits_day = Todo.query.all()
    print(current_user.is_admin)
    if bool(exits_day) == False:
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for day in days_of_week:
            new_todo = Todo(day=day)
            db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('main.home'))
    else:
        days = {}
        allday = Todo.query.all()
        for day in allday:
            days[day.id - 1] = day.day
        # cho vào từ điển . vì id trong bảng bắt đầu từ 1 nên key phảii trừ đi 1 
        sorted_dict = {k: v for k, v in sorted(days.items(), key=lambda item: item[1])}
        if request.method == "POST":
            if 'next' in request.form:
                current_index = session.get('current_index' ,0)  # lần đầu tuyên truy cập trang web sẽ luôn trả về  thữ 2 
                current_index = (current_index +1) % len(days)
                session['current_index'] = current_index
            elif 'forward' in request.form:
                current_index = session.get('current_index' , 0)
                current_index = (current_index-1) % len(days)
                session['current_index'] = current_index
        #id = 0 : monday ....6: sunday...........
        current_index  = session.get('current_index' , 0)
        current_day = days[current_index]
    # Truy cập đối tượng Todo với day='Saturday'
        todo = Todo.query.filter_by(day=current_day).first()
# Lấy danh sách các task liên kết với ngày đó
        tasks = todo.tasks

        return render_template('base.html' , days = days  , current_day = current_day  , tasks =tasks )
        

@main_bl.route('/addtask/<day>', methods=['POST', 'GET'])
@login_required
def addtask(day):
    # Truy cập đối tượng Todo với day='Saturday'
    d_day = Todo.query.filter_by(day=day).first() 
    # Lấy danh sách các task liên kết với ngày đó
# In ra nội dung của các task
    if request.method == "POST":
        try:
            new = request.form['task']
            new_task = Task(content = new , todo_id = d_day.id)
            db.session.add(new_task)
            db.session.commit()
        except:
            return  redirect(url_for('main.home'))
            
    return  redirect(url_for('main.home'))


@main_bl.route('/delete_task/<id>', methods=['GET', 'POST'])
@login_required
def delete_task(id):
    try:
        task =  Task.query.get(id)
        db.session.delete(task)
        db.session.commit()
    except:
        return redirect(url_for('main.home'))

    return redirect(url_for('main.home'))



@main_bl.route('/add' , methods = ['POST' , 'GET'])
@login_required
def add():
    form  = add_student()
    print(form.data)
    if form.validate_on_submit():
        exit_student = User_base.query.filter_by(user_name = form.user_name.data).first()
        print(exit_student)
        if not exit_student :
            username = form.name.data
            date_of_birth = form.date_of_birth.data
            age = form.age.data
            gender = form.gender.data
            nationality = form.nationnality.data
            address = form.address.data
            email = form.email.data
            phone_number = form.phone_number.data
            class_st = form.Class.data
            stu_username = form.user_name.data
            password = form.password.data
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User_base(user_name =  stu_username  , password = hashed_password) 
            db.session.add(new_user)
            db.session.flush()
            new_student = Student(Name = username , Date_of_birth = date_of_birth , age = age , Gender = gender  , Nationality = nationality , Address  =address , Email = email , Phone_number = phone_number ,Class = class_st  ,User_id = new_user.id )
            db.session.add(new_student)
            db.session.commit()
            return redirect(url_for('main.students'))
        
        else:
            flash('tạo tài khoản không thành công ', 'error')
    return render_template('add.html' , form  = form)





@main_bl.route('/students' , methods = ['POST' , 'GET'])
@login_required
def students():
    students = Student.query.all()
    return render_template('students.html' , students = students)



@main_bl.route('/students/<int:id>')
@login_required
def student_detail(id):
    student = Student.query.get(id)
    return render_template('student_activity.html' , student = student)
@main_bl.route('/update_activity/<int:id>' ,methods = ['POST' , 'GET'])
@login_required
def update_activity(id):
    
    student = Student.query.get(id)
    print(student.Student_activity)
    user = User_base.query.get(student.id)
    new = request.form['activity']
    if student.Student_activity:
        student.Student_activity += "\n" +  new 
    else:
        student.Student_activity = new
    db.session.commit()
    return render_template('student_activity.html' , student = student)
  
@main_bl.route('/delete/<int:id>' ,methods = ['POST' , 'GET'])

@login_required
def delete_student(id):
    try:
        student = Student.query.get(id)
        user  = User_base.query.get(student.User_id)
        if student and user:
            db.session.delete(student)
            db.session.delete(user)
    except:
        flash('can not delete')
        return render_template('student_activity.html' , student  = student)
    db.session.commit()
    return redirect(url_for('main.students'))
@main_bl.route('/update_student/<int:id>', methods = ['POST' , 'GET'])
@login_required
def update_stu(id):
    student = Student.query.get(id)
    print(type(student))
    if request.method == "POST":
        try:
            new = request.form.to_dict() 
            for key , value in new.items():
                if getattr(student , key) != value: # getattr dùng để lấy một giá trị của 1 object 
                    #so sánh các giá trị của lớp student cũ , và giá trị người dùng nhập vào từ fom
                    setattr(student , key , value) # key là các thuộc tính, value là các giá trị mối 
            db.session.commit()
        except:
            return render_template('student_activity' , student =student)
    return render_template('student_activity.html' , student = student)

