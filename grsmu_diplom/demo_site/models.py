from django.db import models
from users.models import Profile
from django.contrib.auth.models import User



# Create your models here.
class Department(models.Model):
    title = models.CharField(max_length=120)

    def __str__(self):
        return self.title

class Teacher(models.Model):
    name = models.CharField(max_length=50)
    position = models.CharField(max_length=40)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    teacher_img = models.ImageField(null=True, blank=True, upload_to='teacher_pics')
    image_src = models.CharField(max_length=100, default="0")
    communication_average = models.DecimalField(default=0, max_digits=2, decimal_places=1)
    teaching_average = models.DecimalField(default=0, max_digits=2, decimal_places=1)
    demanding_average = models.DecimalField(default=0, max_digits=2, decimal_places=1)

    def __str__(self):
        return self.name

class Comment(models.Model):
    author = models.CharField(max_length=30)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)

class CommentAnswer(models.Model):
    author = models.CharField(max_length=30)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    communication = models.IntegerField(default=0)
    teaching = models.IntegerField(default=0)
    demanding = models.IntegerField(default=0)

