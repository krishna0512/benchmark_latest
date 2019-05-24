from django.db import models
#from .search import BookIndex
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from zipfile import ZipFile
import os
import shutil
from fpdf import FPDF
from django.core.files import File
# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=200,default="")
    author = models.CharField(max_length=200,default="")
    isbn = models.CharField(max_length=20, blank=True)
    numpages = models.CharField(max_length=20,default="")
    publisher = models.CharField(max_length=200, blank=True)
    editor = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    language = models.CharField(max_length=20, blank=True)
    thumbnail = models.ImageField(upload_to='media/', blank=True,null = True)
    genre = models.CharField(max_length=200,blank=True)
    source = models.CharField(max_length=200,blank=True)
    book_pdf = models.FileField(upload_to="book_pdf",blank=True,null=True)
    # open_books = models.FileField(upload_to="pdfs",blank=True)

    #initiate the class 
    # a = Page.init()

    def __repr__(self):
        return '<Book: {} ({})>'.format(self.title, self.id)

    def __str__(self):
        return '<Book: {} ({})>'.format(self.title, self.id)

@receiver(post_save, sender=Book)
def convert_zipimages_pdf(sender, instance, **kwargs):
    print(instance.book_pdf.path)
    if instance.book_pdf.path.split('.')[-1] == 'pdf':
        return None
    with ZipFile(instance.book_pdf.path, 'r') as zp:
        names=zp.namelist()
        foldername=names[0]
        del names[0]
        for i in names:
            print(i)
        a=instance.book_pdf.path.split('/')
        del a[-1]
        a='/'.join(a)
        print(os.getcwd())
        if 'media/book_pdf' not in os.getcwd():
            os.chdir('media/book_pdf')
        zp.extractall(a)
        pdf=FPDF()
        for image in names:
            print(image)
            pdf.add_page()
            pdf.image(image,0,0,210,297)
        print('Done')
        filename = instance.book_pdf.path.split('/')[-1].split('.')[0]+'.pdf'
        pdf.output('/tmp/'+filename,'F')
        shutil.rmtree('/'.join(instance.book_pdf.path.split('/')[:-1])+'/'+foldername)
        instance.book_pdf.delete(False)
        instance.book_pdf.save(filename, File(open('/tmp/'+filename, 'rb')))

class Page(models.Model):
    # pagetitle stores the name of the text file from which the body contents come from.
    pagetitle = models.CharField(max_length=100, default='')
    book = models.ForeignKey("Book", on_delete=models.CASCADE, related_name='pages')
    content = models.TextField()

    def __str__(self):
        return '<Page: {} ({})'.format(self.pagetitle, self.book.title)

# page_model = Page()

