from __future__ import absolute_import

from celery import shared_task
from celery import task


#from celery.task import tasks
#from celery.task import Task

@task()
#@shared_task
def add():
    print ("add")

@shared_task
def mul():
    print("mul")


@shared_task
def sub():
    print("sub")
