from author.decorators import with_author
from django.contrib.auth.models import AbstractUser
from django.db import models
from django_extensions.db.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField


@with_author
class User(AbstractUser, TimeStampedModel):
    def __str__(self):
        return f"{self.username} - {self.email}"


@with_author
class Profile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone = PhoneNumberField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} {self.user.email}"
