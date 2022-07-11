from django.db import models

# Create your models here.

class Question(models.Model):
    body = models.CharField(max_length=200)
    subject = models.CharField(max_length=200, default='-')
    topic = models.CharField(max_length=200, default='-')
    answers = models.ManyToManyField ('Answer', related_name='answers')

    def __str__(self):
        return self.body


class Answer(models.Model):
    body = models.CharField(max_length=200)

    def __str__(self):
        return self.body

