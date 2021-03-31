from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Supervisor, Student

# Create your views here.
def signin(request):
    return render(request, 'user/login.html')
    
def verify(request):
    if not request.user.is_authenticated:    
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
    else:
        user = request.user
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        if hasattr(user.seu_user, 'student'):
            return HttpResponseRedirect(reverse('user:supervisor_detail'))
        elif hasattr(user.seu_user, 'supervisor'):
            return HttpResponseRedirect(reverse('user:student_detail'))
        else:
            return HttpResponse("Invalid User")
            return HttpResponseRedirect(reverse('user:login'))
    else:
        # Return an 'invalid login' error message.
        return HttpResponse("Invalid password or username")
        return HttpResponseRedirect(reverse('user:login'))
        
def signout(request):
    logout(request) 
    return HttpResponseRedirect(reverse('user:login'))

@login_required
def supervisor_detail(request):
    seu_user = request.user.seu_user
    if not hasattr(seu_user, 'student'):
        return HttpResponse("You are not a student!")
    if seu_user.student.is_picked:
        return HttpResponseRedirect(reverse('user:studentend_result'))
    supervisors_available = Supervisor.objects.filter(headcount__gt=0)
    template = loader.get_template('user/supervisor_detail.html')
    context = {'supervisors':supervisors_available, 'seu_user':seu_user}
    return HttpResponse(template.render(request=request, context=context))
    
@login_required
def pick_supervisor(request):
    seu_user = request.user.seu_user
    if not hasattr(seu_user, 'student'):
        return HttpResponse("You are not a student!")
    if seu_user.student.is_picked:
        return HttpResponse("You have been picked!")
        return HttpResponseRedirect(reverse('user:studentend_result'))
    if seu_user.student.is_pick_recently():
        return HttpResponse("Pick recently!")
        return HttpResponseRedirect(reverse('user:studentend_result'))
    
        
    try:
        picked_supervisor = Supervisor.objects.get(pk=request.POST['choice'])
    except(KeyError, Supervisor.DoesNotExist):
        return HttpResponse("Invalid supervisor!")
        return HttpResponseRedirect(reverse('user:supervisor_detail'))
    seu_user.student.my_supervisor = picked_supervisor
    seu_user.student.pick_time = timezone.now()
    seu_user.student.save()
    print(seu_user.student.my_supervisor.auth_user.username)
    return HttpResponseRedirect(reverse('user:studentend_result'))

@login_required
def studentend_result(request):
    seu_user = request.user.seu_user
    if not hasattr(seu_user, 'student'):
        return HttpResponse("You are not a student!")
    if not seu_user.student.my_supervisor:
        return HttpResponse("havn't pick an supervisor yet!")
        return HttpResponseRedirect(reverse('user:supervisor_detail'))
    return render(request, 'user/studentend_result.html', {'seu_user':seu_user})

@login_required
def student_detail(request):
    seu_user = request.user.seu_user
    if not hasattr(seu_user, 'supervisor'):
        return HttpResponse("You are not a supervisor!")
    student_list = seu_user.supervisor.student_set.all()
    waiting_list = student_list.filter(is_picked=False)
    picked_list = student_list.filter(is_picked=True)
    context = {'seu_user':seu_user, 'waiting_list':waiting_list, 'picked_list':picked_list}
    return render(request, 'user/student_detail.html', context)

@login_required
def pick_student(request):
    seu_user = request.user.seu_user
    if not hasattr(seu_user, 'supervisor'):
        return HttpResponse("You are not a supervisor!")
    if seu_user.supervisor.headcount == 0:
        HttpResponseRedirect(reverse('user:student_detail'))
    try:
        picked_student = Student.objects.get(pk=request.POST['choice'])
    except(KeyError, Supervisor.DoesNotExist):
        return HttpResponseRedirect(reverse('user:student_detail'))
    seu_user.supervisor.headcount -= 1
    picked_student.is_picked = True
    picked_student.save()
    seu_user.supervisor.save()
    return HttpResponseRedirect(reverse('user:student_detail'))