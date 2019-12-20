from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
import os


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('profile/', filename)
# Create your models here.


class House(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.TextField()
    GUID = models.TextField()

    class Meta:
        ordering = ('id',)


class Profile(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to=get_file_path)
    name = models.TextField(max_length=500, blank=True)
    house = models.ForeignKey(House, on_delete=models.CASCADE)


class Accessories(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.TextField()
    channel = models.IntegerField()
    pos = models.IntegerField()
    status = models.IntegerField(default=0)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    iconName = models.TextField()
    AccType = models.IntegerField()
    
    isAnalog = models.BooleanField(default=False)
    analogValue = models.IntegerField()
    isActive = models.IntegerField(default=1)

    class Meta:
        ordering = ('id',)


class AccessoryGroups(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.TextField()
    iconName = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    accessories = models.ManyToManyField(Accessories)

    class Meta:
        ordering = ('id',)


class Scenes(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.TextField()
    iconName = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(AccessoryGroups, on_delete=models.CASCADE)


class Command(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    command = models.BooleanField(default=False)
    accessory = models.ForeignKey(Accessories, on_delete=models.CASCADE)
    scene = models.ForeignKey(
        Scenes, related_name='commands', on_delete=models.CASCADE)

