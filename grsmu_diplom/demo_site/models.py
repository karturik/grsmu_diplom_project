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
    department = models.ForeignKey('Department', on_delete=models.CASCADE, related_name='FromDepartment')
    teacher_img = models.ImageField(null=True, blank=True, upload_to='teacher_pics', default='teacher.jpg')
    image_src = models.CharField(max_length=100, default="0")
    communication_average = models.FloatField(default=0.0)
    teaching_average = models.FloatField(default=0.0)
    demanding_average = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='CommentFrom')
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, related_name='CommentFor')
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')
    CATEGORY_CHOICES = (
        ('lesson', 'Занятия'),
        ('lection', 'Лекции'),
        ('exam', 'Экзамены'),
        ('other', 'Остальное'),
    )
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='other')
    checked = models.BooleanField(default=False)

    def __str__(self):
        return self.body



class CommentAnswer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name = "AnswerFor")
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)

    def __str__(self):
        return self.body


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='VoteFrom')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='VoteFor')
    communication = models.IntegerField(default=0)
    teaching = models.IntegerField(default=0)
    demanding = models.IntegerField(default=0)

