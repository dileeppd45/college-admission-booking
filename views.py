from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from django.db import connection
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from . import views

def login(request):
    if request.method == "POST":
        userid = request.POST['userid']
        password = request.POST['password']
        cursor = connection.cursor()
        cursor.execute("select * from login where admin_id= '" + userid + "' AND password = '" + password + "'")
        admin = cursor.fetchone()
        if admin == None:
            cursor.execute("select * from college where idcollege= '" + userid + "' AND password = '" + password + "' and status ='approved'")
            college = cursor.fetchone()
            if college == None:
                cursor.execute("select * from student  where idstudent ='"+ userid +"' and password ='"+ password +"' ")
                student = cursor.fetchone()
                if student == None:
                    return HttpResponse("<script>alert('Invalid User or not approved yet..');window.location='../login';</script>")

                else:
                    request.session['studid'] = userid
                    return redirect('student_home')

            else:
                request.session['colid'] = userid
                return redirect('college_home')
        else:
            request.session['adminid'] = userid
            return redirect('admin_home')
    return render(request, "login.html")




def admin_home(request):
    return render(request, 'admin_home.html')

def approved_colleges(request):
    cursor=connection.cursor()
    cursor.execute("select * from college where status ='approved'")
    data=cursor.fetchall()
    return render(request,'admin_approved_colleges.html',{'data':data})

def pending_colleges(request):
    cursor=connection.cursor()
    cursor.execute("select * from college where status ='pending'")
    data=cursor.fetchall()
    return render(request,'admin_pending_colleges.html',{'data':data})
def approve_college(request, id):
    cursor = connection.cursor()
    cursor.execute("update college set status='approved' where idcollege = '"+str(id)+"' ")
    return redirect('pending_colleges')

def register_department(request):
    return render(request, 'admin_register_department.html')

def add_department(request):
    if request.method =="POST":
        name = request.POST['dname']
        cursor=connection.cursor()
        cursor.execute("insert into department values(null,'"+str(name)+"' )")
    return redirect('view_department')

def view_department(request):
    cursor = connection.cursor()
    cursor.execute("select * from department")
    department = cursor.fetchall()
    return render(request,'admin_view_department.html',{'data':department})

def edit_department(request, id):
    return render(request, 'admin_edit_department.html', {'id':id})

def update_department(request):
    if request.method=="POST":
        name = request.POST['dname']
        did=request.POST['did']
        cursor = connection.cursor()
        cursor.execute("update department set name='" + str(name) + "' where iddepartment='" + str(did) + "' ")
        return redirect('view_department')

def remove_department(request, id):
    cursor = connection.cursor()
    cursor.execute("delete from departments where iddepartment='" + str(id) + "' ")
    return redirect('view_department')

def reg_course(request, id):
    return render(request, 'admin_register_course.html',{'id':id})

def add_course(request):
    if request.method =="POST":
        name = request.POST['cname']
        did = request.POST['did']
        cursor = connection.cursor()
        cursor.execute("insert into course values(null,'" + str(name) + "', '" + str(did) + "') ")
    return redirect('view_course', id=int(did))

def view_course(request, id):
    cursor=connection.cursor()
    cursor.execute("select * from course where iddepartment ='"+str(id)+"' ")
    course= cursor.fetchall()
    return render(request, 'admin_view_course.html',{'data':course})

def edit_course(request, id):
    cursor =connection.cursor()
    return render (request, 'admin_edit_course.html', {'id':id})

def update_course(request):
    if request.method=="POST":
        name = request.POST['cname']
        cid=request.POST['cid']
        cursor = connection.cursor()
        cursor.execute("update course set name='"+str(name)+"' where idcourse='"+str(cid)+"' ")
        return redirect('view_course', id=int(did))

def remove_course(request, id):
    cursor = connection.cursor()
    cursor.execute("delete from course where idcourse='" + str(id) + "' ")
    return redirect('view_course',id=int(did))

def register_college(request):
    return render(request,'reg_college.html')

def add_college(request):
    if request.method=="POST":
        name = request.POST['col_name']
        col_id = request.POST['col_id']
        address = request.POST['col_address']
        phone = request.POST['col_phone']
        email = request.POST['col_email']
        col_lat = request.POST['col_lat']
        col_lon = request.POST['col_lon']
        col_password = request.POST['col_password']
        cursor = connection.cursor()
        cursor.execute("select * from college where idcollege ='"+str(col_id)+"' ")
        data=cursor.fetchone()
        if data == None:
            cursor.execute("select * from login where admin_id ='" + str(col_id) + "' ")
            data = cursor.fetchone()
            if data == None:
                cursor.execute("select * from student where idstudent ='" + str(col_id) + "' ")
                data = cursor.fetchone()
                if data == None:
                    cursor.execute("insert into college values ('" + str(col_id) + "','" + str(name) + "', '" + str(address) + "', '" + str(phone) + "','" + str(email) + "','" + str(col_password) + "','" + str(col_lat) + "','" + str(col_lon) + "','pending')")
                    return render(request, "login.html")
        else:
            return HttpResponse("<script>alert('id already exists..  please enter a unique id');window.location='register_college';</script>")





def college_home(request):
    return render(request, 'college_home.html')

def college_choose_department(request):
    cursor=connection.cursor()
    cursor.execute("select * from department")
    department=cursor.fetchall()
    return render(request,'college_choose_department.html',{'data':department})

def college_add_department(request, id):
    college_id = request.session['colid']
    cursor=connection.cursor()
    cursor.execute("select * from college_department where iddepartment='"+str(id)+"' and college_id='" +str(college_id)+ "' ")
    data=cursor.fetchone()
    if data==None:
        cursor.execute("insert into college_department values(null,'"+str(college_id)+"','"+str(id)+"') ")
    return redirect('college_choose_department')


def college_view_department(request):
    cursor=connection.cursor()
    college_id = request.session['colid']
    cursor.execute("SELECT college_department.idcollege_department, department.name, department.iddepartment from college_department  join department on college_department.iddepartment = department.iddepartment where college_department.college_id = '"+str(college_id)+"' ")
    department=cursor.fetchall()
    return render(request,'college_view_department.html', {'data':department})

def college_choose_course(request, id):
    cursor=connection.cursor()
    request.session['coldepid'] = id
    cursor.execute("select * from course where iddepartment='"+str(id)+"' ")
    course=cursor.fetchall()
    return render(request, 'college_choose_course.html',{'data':course})


def college_add_course(request, id):
    cursor = connection.cursor()
    college_id = request.session['colid']
    did = request.session['coldepid']
    cursor.execute("select * from college_course where iddepartment = '"+str(did)+"' and idcourse = '"+str(id)+"' and college_id = '"+str(college_id)+"' ")
    data=cursor.fetchone()
    if data== None:
        cursor.execute("insert into college_course values (null, '"+str(did)+"', '"+str(id)+"', '"+str(college_id)+"','pending','pending' )")
    return redirect('college_choose_course', id=int(did))

def college_view_course(request,id):
    cursor=connection.cursor()
    request.session['departid'] =id
    college_id = request.session['colid']
    cursor.execute("SELECT college_course.idcollege_course, course.name , college_course.seats, college_course.seat_count,college_course.idcourse from course  join college_course on college_course.idcourse = course.idcourse where college_course.college_id = '"+str(college_id)+"'and college_course.iddepartment='"+str(id)+"' ")
    course =cursor.fetchall()
    return render(request,'college_view_course.html', {'data':course})

def update_seats(request, id):
    cursor = connection.cursor()
    college_id = request.session['colid']
    cursor.execute("SELECT college_course.idcollege_course, course.name , college_course.seats from course  join college_course on college_course.idcourse = course.idcourse where college_course.college_id = '"+str(college_id)+"'and college_course.idcollege_course ='"+str(id)+"'")
    data=cursor.fetchone()
    return render(request, 'college_update_seats.html',{'row':data})

def seat_update(request):
    if request.method == "POST":
        college_id = request.session['colid']
        did=request.session['departid']
        id = request.POST['colcoid']
        seat = request.POST['seat']
        cursor=connection.cursor()
        cursor.execute(" update college_course set seats ='"+str(seat)+"' where idcollege_course = '"+str(id)+"' ")
        cursor.execute("select * from course_booking where idcollege = '"+str(college_id)+"' and idcourse = '"+str(id)+"' ")
        data = cursor.fetchall()
        count = int(0)
        for i in data:
            count = count +1

        cursor.execute("update college_course set seat_count = '"+str(count)+"' where idcollege_course ='"+str(id)+"' ")            

        return redirect('college_view_course',id=int(did))


def register_student(request):
    return render(request,'reg_student.html')

def add_student(request):
    if request.method == "POST":
        stud_id=request.POST['stud_id']
        name = request.POST['stud_name']
        address = request.POST['stud_address']
        phone = request.POST['stud_phone']
        email = request.POST['stud_email']
        password = request.POST['password']
        cursor = connection.cursor()
        cursor.execute("select * from college where idcollege ='" + str(stud_id) + "' ")
        data = cursor.fetchone()
        if data == None:
            cursor.execute("select * from login where admin_id ='" + str(stud_id) + "' ")
            data = cursor.fetchone()
            if data == None:
                cursor.execute("select * from student where idstudent ='" + str(stud_id) + "' ")
                data = cursor.fetchone()
                if data == None:
                    cursor.execute("insert into student values ('"+str(stud_id)+"','" + str(name) + "','" + str(address) + "','" + str(phone) + "','" + str(email) + "','"+str(password)+"' )")
        else:
            return HttpResponse("<script>alert('id already exists..  please enter a unique id');window.location='register_student';</script>")

    return redirect("login")


def student_home(request):
    return render(request, 'student_home.html')

def stud_view_college(request):
    cursor=connection.cursor()
    cursor.execute("select * from college where status ='approved' ")
    data= cursor.fetchall()
    return render(request, 'student_view_college.html',{'college':data} )

def student_view_department(request,id):
    request.session['studviewcollegeid'] =str(id)
    cursor=connection.cursor()
    cursor.execute("SELECT college_department.idcollege_department, department.name, department.iddepartment from college_department  join department on college_department.iddepartment = department.iddepartment where college_department.college_id = '"+str(id)+"' ")
    data= cursor.fetchall()

    return render(request, 'student_view_department.html',{'department':data})

def student_view_course(request,id):
    college_id = request.session['studviewcollegeid']
    cursor = connection.cursor()
    cursor.execute("SELECT college_course.idcollege_course, course.name , college_course.seats, college_course.idcourse, college_course.seat_count from course  join college_course on college_course.idcourse = course.idcourse where college_course.college_id = '" + str(college_id) + "'and college_course.iddepartment='" + str(id) + "' and college_course.seats !='pending' ")
    data=cursor.fetchall()
    return render(request, 'student_view_course.html', {'course':data, 'colid':college_id})

def stud_book_course(request, id):
    cursor = connection.cursor()
    college_id = request.session['studviewcollegeid']
    cursor.execute("select seats, idcourse from college_course where college_id = '"+str(college_id)+"' and idcollege_course = '"+str(id)+"' ")
    total_seat=cursor.fetchone()
    seat=list(total_seat)
    total_seat=int(seat[0])
    idcourse =int(seat[1])
    print(total_seat)
    cursor.execute("select * from course_booking where idcollege ='"+str(college_id)+"' and idcourse ='"+str(idcourse)+"' ")
    data1=cursor.fetchall()
    data1=list(data1)
    count = int(0)
    for i in data1:
        count=count+1
    if count < total_seat:
        cursor.execute("select * from account_table where account_id ='1' ")
        data = cursor.fetchone()
        return render(request, 'stud_book_course.html', {'id': idcourse,'id_col_course': id, 'row': data})
    else:
        return HttpResponse("<script>alert('No more seats available..');window.location='../stud_view_college';</script>")


def book_proceed(request):
    if request.method == "POST":
        college_id = request.session['studviewcollegeid']
        card_no=request.POST['card_no']
        course_id = request.POST['course_id']
        id_col_course = request.POST['id_col_course']
        student = request.session['studid']
        holder = request.POST['card_holder']
        exp = request.POST['card_expiry']
        cvv = request.POST['card_cvv']
        cursor = connection.cursor()
        cursor.execute("select * from account_table where card_number ='"+str(card_no)+"' and card_holder_name = '"+str(holder)+"' and  card_expiry_date= '"+str(exp)+"' and card_cvv = '"+str(cvv)+"' ")
        data = cursor.fetchone()
        if data ==None:
            return HttpResponse("<script>alert('Invalid  Card Entry ');window.location='stud_view_college';</script>")
        else:
            cursor.execute("insert into course_booking values(null,'"+str(course_id)+"','"+str(student)+"', curdate(), '10000', '"+str(college_id)+"')")
            cursor.execute("select * from course_booking where idcollege = '"+str(college_id)+"' and idcourse = '"+str(course_id)+"' ")
            data = cursor.fetchall()
            count = int(0)
            for i in data:
                count = count +1
            print('hdfdfs')
            print(count)
            print('hdfdfs')
            print(course_id)
            cursor.execute("update college_course set seat_count = '"+str(count)+"' where idcollege_course ='"+str(id_col_course)+"' ")
            return redirect('stud_view_college')

def student_booked(request):
    student = request.session['studid']
    cursor=connection.cursor()
    cursor.execute("select course.name,course_booking.* from course_booking join course on course_booking.idcourse = course.idcourse where course_booking.idstudent ='"+str(student)+"' ")
    data= cursor.fetchall()
    return render(request,'student_booked.html',{'data':data})

def student_send_feedback(request,id):
    return render(request,'student_send_feedback.html',{'id':id})

def student_send_fb(request):
    if request.method == "POST":
        college_id = request.POST['colid']
        feedback=request.POST['fb']
        student = request.session['studid']
        cursor = connection.cursor()
        cursor.execute("insert into feedback values(null, '"+str(student)+"', '"+str(feedback)+"', curdate(),'"+str(college_id)+"' )")
        return redirect('student_view_feedback',id= college_id)

def student_view_feedback(request,id):
    cursor = connection.cursor()
    student = request.session['studid']
    cursor.execute("select * from feedback where student='"+str(student)+"' and college='"+str(id)+"' ")
    data = cursor.fetchall()
    return render(request,'student_view_feedback.html',{'data':data})

def college_view_feedback(request):
    cursor = connection.cursor()
    college_id =  request.session['colid']
    cursor.execute("select * from feedback where college = '"+str(college_id)+"' ")
    data = cursor.fetchall()
    print(data)
    return render(request,'college_view_feedback.html',{'data':data})

def college_course_booked(request,id):
    cursor = connection.cursor()
    college_id = request.session['colid']
    cursor.execute("select course.name,course_booking.* from course_booking join course on course_booking.idcourse = course.idcourse where course_booking.idcollege ='"+str(college_id)+"' and course_booking.idcourse ='"+str(id)+"' ")
    data = cursor.fetchall()
    return render(request, 'college_course_booked.html',{'data':data})

def admin_view_department(request,id):
    request.session['adminviewcollegeid'] =str(id)
    cursor=connection.cursor()
    cursor.execute("SELECT college_department.idcollege_department, department.name, department.iddepartment from college_department  join department on college_department.iddepartment = department.iddepartment where college_department.college_id = '"+str(id)+"' ")
    data= cursor.fetchall()

    return render(request, 'admin_view_departmentc.html',{'department':data})

def admin_view_coursesc(request,id):
    college_id = request.session['adminviewcollegeid']
    cursor = connection.cursor()
    request.session['adminviewdepid'] = id
    cursor.execute("SELECT college_course.idcollege_course, course.name , college_course.seats, college_course.idcourse, college_course.seat_count from course  join college_course on college_course.idcourse = course.idcourse where college_course.college_id = '" + str(college_id) + "'and college_course.iddepartment='" + str(id) + "' and college_course.seats !='pending' ")
    data=cursor.fetchall()
    return render(request, 'admin_view_coursec.html', {'course':data, 'colid':college_id})

def admin_view_course_booked(request,id):
    cursor = connection.cursor()
    did = request.session['adminviewdepid']
    college_id = request.session['adminviewcollegeid']
    cursor.execute("select course.name,course_booking.* from course_booking join course on course_booking.idcourse = course.idcourse where course_booking.idcollege ='"+str(college_id)+"' and course_booking.idcourse ='"+str(id)+"' ")
    data = cursor.fetchall()

    return render(request, 'admin_view_course_booked.html',{'data':data,'did':did})
