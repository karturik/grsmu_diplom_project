from django.db import models

# Create your models here.
class Department(models.Model):
    title = models.CharField(max_length=120)

class Teacher(models.Model):
    name = models.CharField(max_length=50)
    position = models.CharField(max_length=40)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    teacher_pic = models.ImageField(null=True, blank=True, upload_to='teacher_pics', default='user.jpg')

class Comment(models.Model):
    author = models.CharField(max_length=30)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
