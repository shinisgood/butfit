from django.db import models
from django.contrib.auth.models import AbstractUser

from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager

use_days = (
    ("30", "30"),
    ("60", "60"),
    ("90", "90"),
)


class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    # phone_number = models.CharField(max_length=12, unique=True)

    # USERNAME_FIELD = "phone_number"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
        # return self.phone_number

    class Meta:
        db_table = "users"
        app_label = "users"


class Credit(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("User", models.DO_NOTHING)
    credit = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    use_days = models.CharField(max_length=10, choices=use_days, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "credits"
        app_label = "users"


class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("User", models.DO_NOTHING, null=True, blank=True)
    course = models.ForeignKey(
        "courses.Course", models.DO_NOTHING, null=True, blank=True
    )
    is_canceled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "reservations"
        app_label = "users"
