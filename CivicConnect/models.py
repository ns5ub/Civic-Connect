from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from multiselectfield import MultiSelectField

interests = [('1', "Cybersecurity"), ('2', "Police Brutality")]


class Interest(models.Model):
    description = models.CharField(max_length=300)
    def __str__(self):
        return self.description


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    address = models.CharField(max_length=30, blank=True)
    interests = models.ManyToManyField(Interest, default=[])
    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class TemplateSubmission(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE,  blank=True, null=True, default=None)
    topic = models.CharField(max_length=100, blank=True)
    template = models.TextField(max_length=5000, blank=True)
    date_posted = models.DateTimeField(auto_now=True)
    associated_interests = models.ManyToManyField(Interest, default=[])
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.template
