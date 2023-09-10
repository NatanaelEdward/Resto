from django.db import models
from django.contrib.auth.models import User
# Create your models here.

Roles = (
    ('manajer', 'manajer'),
    ('kasir', 'KASIR'),
    ('user', 'USER')
)

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,    default=None, null=True)
    role = models.CharField(max_length=50, choices=Roles, default='kasir')

    def __str__(self):
        return self.user.username