import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CLIENT = 'client'
    ROLE_DEVELOPER = 'developer'
    ROLE_CHOICES = [
        (ROLE_CLIENT, 'Client'),
        (ROLE_DEVELOPER, 'Developer'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    @property
    def is_client(self):
        return self.role == self.ROLE_CLIENT

    @property
    def is_developer(self):
        return self.role == self.ROLE_DEVELOPER
