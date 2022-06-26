from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.CharField(max_length=255, default='images/user.jpg')
    course = models.IntegerField(default=0)
    warnings = models.IntegerField(default=0)

    def warnings_delete(self, request):
        if self.warnings == 3:
            user = User.objects.get(id = request.user.id)
            user.delete()

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwagrs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwagrs):
        instance.profile.save()