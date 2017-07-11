# Create your tasks here
from __future__ import absolute_import
from celery import shared_task


@shared_task
def add(x, y):
    print(x+y)
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)

add.delay(7, 8)