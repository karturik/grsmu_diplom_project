from django.db import models

# Create your models here.
class Department(models.Model):
    title = models.CharField(max_length=120)

class Teacher(models.Model):
    name = models.CharField(max_length=50)
    position = models.CharField(max_length=40)
    departments = models.ForeignKey('Department', on_delete=models.CASCADE)

class Comment(models.Model):
    author = models.CharField(max_length=20)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
