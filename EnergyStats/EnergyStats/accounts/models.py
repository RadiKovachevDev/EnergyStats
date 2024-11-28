from django.contrib.auth.models import AbstractUser
from django.db import models

class EnergyUser(AbstractUser):
    USER_ROLES = (
        ('member', 'Member'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=USER_ROLES, default='member')

    def is_member(self):
        return self.role == 'member'

    def is_admin(self):
        return self.role == 'admin'
