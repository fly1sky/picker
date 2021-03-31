import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class SEU_User(models.Model):
    auth_user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        primary_key=True
    )
    
    def __str__(self):
        return self.auth_user.username
        
class Supervisor(SEU_User):
    headcount = models.IntegerField(default=0)

class Student(SEU_User):
    my_supervisor = models.ForeignKey(
        Supervisor, on_delete=models.SET_NULL, 
        blank=True, null=True
    )
    pick_time = models.DateTimeField('pick time', null=True, blank=True)
    is_picked = models.BooleanField(default=False)
    
    def is_pick_recently(self):
        return self.pick_time and timezone.now() <= datetime.timedelta(seconds=3) + self.pick_time
    
    

    