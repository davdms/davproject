from quotes.models import Quotes, Authors, Tags

from celery import shared_task


# @shared_task
# def add(x, y):
#     return x + y