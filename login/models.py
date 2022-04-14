from email.policy import default
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class user_details(models.Model):
     user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
     phone = models.IntegerField()
     Address = models.CharField(max_length=220)
     DOB = models.DateField()
     image=models.ImageField(upload_to='image/',null=True)

class reason(models.Model):
     leavereason=models.CharField(max_length=200)

class Leave(models.Model):
     user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
     reason = models.ForeignKey(reason,on_delete=models.CASCADE,null=True)
     status = models.CharField(max_length=30,default='pending')
     reasondate=models.DateField()
class employee(models.Model):
     role=models.CharField(max_length=200)  

class Employeedetails(models.Model):
     user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)  
     employee = models.ForeignKey(employee,on_delete=models.CASCADE,null=True)
     salary=models.IntegerField(default=0)

class course(models.Model):
     UG=models.CharField(max_length=20)
class academic_details(models.Model):
     user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
     course = models.ForeignKey(course,on_delete=models.CASCADE,null=True)
     ugmark =models.IntegerField()

class Task(models.Model):
     user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
     start=models.DateField()
     end=models.DateField()
     work=models.CharField(max_length=50)
     status=models.CharField(max_length=30,default='pending')
