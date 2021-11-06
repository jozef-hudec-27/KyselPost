from django.db import models
from django.contrib.auth.models import AbstractUser


"TERAZ PRIDAJ USER PANEL A TO ZE JEDEN USER BUDE MOCT FOLLOWOVAT DRUHEHO"


class User(AbstractUser):
    username = models.CharField(max_length=200, unique=True)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(null=True, default="avatar.svg")
    followers = models.ManyToManyField("self", blank=True, symmetrical=False)
    
    REQUIRED_FIELDS = []

class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    tag = models.CharField(max_length=50)
    name = models.CharField(max_length=200)
    body = models.TextField(null=False, blank=False)
    likes = models.ManyToManyField(User, related_name="likes", blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return self.name