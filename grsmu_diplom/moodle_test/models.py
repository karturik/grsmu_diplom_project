from django.db import models

# Create your models here.

class Question(models.Model):
    body = models.CharField(max_length=200)
    subject = models.CharField(max_length=200, default='-')
    topic = models.CharField(max_length=200, default='-')

    def __str__(self):
        return self.body


class Answer(models.Model):
    body = models.CharField(max_length=200)
    question = models.ForeignKey('Question', blank=False, related_name='answers', on_delete=models.CASCADE)

    def __str__(self):
        return self.body

