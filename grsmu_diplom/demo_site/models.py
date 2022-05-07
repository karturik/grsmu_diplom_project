from django.db import models
from users.models import Profile


# Create your models here.
class Department(models.Model):
    title = models.CharField(max_length=120)

class Teacher(models.Model):
    name = models.CharField(max_length=50)
    position = models.CharField(max_length=40)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    teacher_pic = models.ImageField(null=True, blank=True, upload_to='teacher_pics', default='user.jpg')
    communication_average = models.DecimalField(default=0, max_digits=3, decimal_places=1)
    teaching_average = models.DecimalField(default=0, max_digits=3, decimal_places=1)
    demanding_average = models.DecimalField(default=0, max_digits=3, decimal_places=1)

class Comment(models.Model):
    author = models.CharField(max_length=30)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)

class Vote(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    communication = models.IntegerField(default=0)
    teaching = models.IntegerField(default=0)
    demanding = models.IntegerField(default=0)

