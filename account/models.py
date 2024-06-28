from django.contrib.auth.models import AbstractUser
from django.db import models

from account.managers import CustomUserManager

sex = (
    ('M', "Male"),
    ('F', "Female"),
)

ROLE = (
    ('employer', "Employer"),
    ('employee', "Employee"),
    ('coordinator', 'Coordinator'),
    ('supervisor', 'Supervisor'),
    ('worksupervisor','Worksupervisor')
)


class User(AbstractUser):
    username = None
    

    email = models.EmailField(unique=True, blank=False, error_messages={'unique': "A user with that email already exists."})
    role = models.CharField(choices=ROLE, max_length=15)
    gender = models.CharField(choices=sex, max_length=1)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
