from django.db import models
from django.contrib.auth.models import User
from menuapp.models import DataMeja
# Create your models here.

Roles = (
    ('manajer', 'manajer'),
    ('kasir', 'KASIR'),
    ('user', 'USER')
)

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,    default=None, null=True)
    role = models.CharField(max_length=50, choices=Roles, default='user')
    data_meja = models.ForeignKey(DataMeja, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username