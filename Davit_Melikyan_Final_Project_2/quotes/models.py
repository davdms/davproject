import hashlib
from datetime import datetime

from django.db import models, connections
from django.contrib.auth.models import User
from django.utils import timezone
from taggit.managers import TaggableManager
# Create your models here.
from Quotes_web.hashing import filenamehashing


def get_file_name(_, filename):
    return '/'.join(['author_images', filenamehashing(filename)])


class Authors(models.Model):
    name = models.CharField(max_length=200, null=False)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    image = models.ImageField(upload_to=get_file_name, null=True, blank=True)

    class Meta:
        db_table = 'authors'

    def __str__(self) -> str:
        return self.name


class Tags(models.Model):
    name = models.CharField(max_length=200, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.PositiveIntegerField(null=True)

    class Meta:
        db_table = 'tags'

    def __str__(self) -> str:
        return self.name


class Quotes(models.Model):
    quote = models.TextField(null=False)
    author = models.ForeignKey(Authors, on_delete=models.DO_NOTHING, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'quotes'

    def __str__(self) -> str:
        return self.quote


class QuotesHistory(models.Model):
    quote = models.IntegerField(null=False)
    quote_text = models.TextField(null=False)
    change_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)

    class Meta:
        db_table = 'history_quotes'


class QuotesToTags(models.Model):
    quote = models.ForeignKey(Quotes, on_delete=models.CASCADE, null=False)
    tag = models.ForeignKey(Tags, on_delete=models.PROTECT, null=False)

    class Meta:
        db_table = 'quotes_to_tags'




