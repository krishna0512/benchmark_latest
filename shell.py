from django.urls import reverse
from django.test.utils import setup_test_environment
from django.contrib.auth.models import User
from django.conf import settings

from benchmark.models import *
from benchmark.forms import *
import requests
import os
import sys
import random
from tabulate import tabulate
import xml.etree.ElementTree as et

setup_test_environment()

from django.test import Client
c = Client()

def updatedb():
    
    if not Document.objects.all():
        print('Populating Document model')
        with open('benchmark/static/benchmark/csv/Document.csv') as f:
            r = f.readlines()
        del r[0]
        r = [i.strip().split(';') for i in r]
        for i in r:
            a = Document()
            a.name = i[0]
            a.description = i[1]
            a.save()
            print(a.id)
    
    if not Language.objects.all():
        print('Populating Language model')
        with open('benchmark/static/benchmark/csv/Language.csv') as f:
            r = f.readlines()
        del r[0]
        r = [i.strip() for i in r]
        for i in r:
            a = Language()
            a.name = i
            a.save()
            print(a.id)
    
    if not Modality.objects.all():
        print('Populating Modality model')
        with open('benchmark/static/benchmark/csv/Modality.csv') as f:
            r = f.readlines()
        del r[0]
        r = [i.strip().split(';') for i in r]
        for i in r:
            a = Document.objects.get(id=int(i[1]))
            a.modality.create(name=str(i[0]))
            a.save()
            print(a.id)
    
    if not Task.objects.all():
        print('Populating Task model')
        with open('benchmark/static/benchmark/csv/Task.csv') as f:
            r = f.readlines()
        del r[0]
        r = [i.strip().split(';') for i in r]
        for i in r:
            a = Document.objects.get(id=int(i[2]))
            a.task.create(name=str(i[0]), description=str(i[1]))
            a.save()
            print(a.id)

    if not TaskCategory.objects.all():
        print('Populating TaskCategory model...', flush=True, end='')
        bulk = []
        for t in Task.objects.all():
            for m in Modality.objects.all():
                if t.document.id != m.document.id:
                    continue
                for l in Language.objects.all():
                    a = TaskCategory()
                    a.task = t
                    a.modality = m
                    a.language = l
                    bulk.append(a)
        TaskCategory.objects.bulk_create(bulk)
        print('Done')

def populate_submission():
    if not TaskCategory.objects.all():
        print('First populate the task category by calling updatedb')
        return
    url = 'http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain'
    s = requests.get(url).content.splitlines()
    s = [i.decode() for i in s]
    bulk = []
    for tc in TaskCategory.objects.all():
        for counter in range(5):
            a = Submission()
            a.task_category = tc
            a.user = User.objects.all()[0]
            a.dataset = Dataset.objects.get(id=random.choices([1,2,3,4])[0])
            a.title = ' '.join(random.choices(s, k=3))
            a.description = ' '.join(random.choices(s, k=20))
            bulk.append(a)
    Submission.objects.bulk_create(bulk)

def populate_resource():
    if Resource.objects.all():
        print('Resource already populated')
        return
    bulk = []
    with open('benchmark/static/benchmark/csv/Resource.csv','r') as f:
        r = f.readlines()
    del r[0]
    r = [i.strip().split(';') for i in r]
    for i in r:
        a = Resource()
        a.title = i[0]
        a.authors = i[1]
        a.year = int(i[2])
        a.page_link = i[3]
        a.pdf_link = i[4]
        bulk.append(a)
    Resource.objects.bulk_create(bulk)

def display(m):
    fields = list(m._meta.get_fields())
    fields = [[i.name, getattr(m,i.name)] for i in fields]
    print(tabulate(fields, headers=['Name','Value']))
