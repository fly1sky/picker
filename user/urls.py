from django.urls import path, include

from . import views

app_name='user'
urlpatterns = [
    path('', views.signin, name='main'),
    path('login/', views.signin, name='login'),
    path('logout/', views.signout, name='logout'),
    path('verify/', views.verify, name='verify'),
    path('supervisor_detail/', views.supervisor_detail, name='supervisor_detail'),
    path('pick_supervisor/', views.pick_supervisor, name='pick_supervisor'),
    path('studentend_result/', views.studentend_result, name='studentend_result'),
    path('student_detail/', views.student_detail, name='student_detail'),
    path('pick_student/', views.pick_student, name='pick_student'),
]