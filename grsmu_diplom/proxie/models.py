from django.db import models

# Create your models here.
class Proxie(models.Model):
    ip = models.CharField(max_length=50, blank=False, unique=True)

    def __str__(self):
        return self.ip