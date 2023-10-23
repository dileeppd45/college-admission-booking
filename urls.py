from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login, name="login"),
    path('login', views.login, name="login"),
    path('admin_home', views.admin_home, name='admin_home'),
    path('register_department', views.register_department, name='register_department'),
    path('add_department', views.add_department, name='add_department'),
    path('view_department', views.view_department, name='view_department'),
    path('edit_department/<int:id>', views.edit_department, name='edit_department'),
    path('update_department', views.update_department, name='update_department'),
    path('remove_department/<int:id>', views.remove_department, name='remove_department'),
    path('approved_colleges', views.approved_colleges, name='approved_colleges'),
    path('pending_colleges', views.pending_colleges, name='pending_colleges'),
    path('approve_college/<str:id>', views.approve_college, name='approve_college'),
    path('reg_course/<int:id>', views.reg_course, name='reg_course'),
    path('add_course', views.add_course, name='add_course'),
    path('view_course/<int:id>', views.view_course, name='view_course'),
    path('edit_course/<int:id>', views.edit_course, name='edit_course'),
    path('update_course', views.update_course, name='update_course'),
    path('remove_course/<int:id>', views.remove_course, name='remove_course'),
    path('admin_view_department/<str:id>', views.admin_view_department, name='admin_view_department'),
    path('admin_view_coursesc/<int:id>', views.admin_view_coursesc, name='admin_view_coursesc'),
    path('admin_view_course_booked/<int:id>', views.admin_view_course_booked, name='admin_view_course_booked'),




    path('register_college', views.register_college, name='register_college'),
    path('add_college', views.add_college, name='add_college'),
    path('college_home', views.college_home, name='college_home'),
    path('college_view_feedback', views.college_view_feedback, name='college_view_feedback'),
    path('college_choose_department', views.college_choose_department, name='college_choose_department'),
    path('college_add_department/<int:id>',views.college_add_department, name='college_add_department'),
    path('college_view_department', views.college_view_department, name='college_view_department'),
    path('college_choose_course/<int:id>', views.college_choose_course, name='college_choose_course'),
    path('college_add_course/<int:id>', views.college_add_course, name='college_add_course'),
    path('college_view_course/<int:id>',views.college_view_course, name='college_view_course'),
    path('college_course_booked/<int:id>', views.college_course_booked, name='college_course_booked'),
    path('update_seats/<int:id>', views.update_seats, name='update_seats'),
    path('seat_update', views.seat_update, name='seat_update'),






    path('register_student', views.register_student, name='register_student'),
    path('add_student', views.add_student, name='add_student'),
    path('student_home', views.student_home, name='student_home'),
    path('stud_view_college', views.stud_view_college, name='stud_view_college'),
    path('student_booked', views.student_booked, name='stud_booked'),
    path('student_view_department/<str:id>', views.student_view_department, name='student_view_department'),
    path('stud_view_courses/<int:id>', views.student_view_course, name='student_view_course'),
    path('stud_book_course/<int:id>', views.stud_book_course, name='stud_book_course'),
    path('book_proceed', views.book_proceed, name='book_proceed'),
    path('student_send_feedback/<str:id>',views.student_send_feedback, name='student_send_feedback'),
    path('student_send_fb', views.student_send_fb, name='student_send_fb'),
    path('student_view_feedback/<str:id>', views.student_view_feedback, name='student_view_feedback'),

]

