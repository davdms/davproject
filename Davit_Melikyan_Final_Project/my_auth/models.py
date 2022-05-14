from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.



def get_file_name1(_, filename):
    now = timezone.now()
    return '/'.join(['tmp', 'y-month', f'{now.year}-{now.month}', filename])


class UserHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=100, null=False)
    is_active = models.BooleanField(null=False, default=True)
    change_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_history'
