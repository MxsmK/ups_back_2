from django.db import models
from django.utils import timezone

class Author(models.Model):
    name = models.CharField(max_length=200)
    foto = models.URLField(max_length=200)
    birth = models.DateField()
    death = models.DateField(default=None)
    books = []
    available = []


    class Meta:
        ordering = ('name', )


class Book(models.Model):
    name = models.CharField(max_length=200)
    max_dur = models.IntegerField(max_length=200)
    cover = models.CharField(max_length=200)
    Author = models.ForeignKey(Author, on_delete=models.CASCADE)


    class Meta:
        ordering = ('name', )


class Reader(models.Model):
    name = models.CharField(max_length=200)
    mail = models.CharField(max_length=254)
    rent = []
    fine = models.IntegerField(default=0)


    class Meta:
        ordering = ('name', )


class Rent(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    time = models.DateField(default=timezone.now)
    dur = models.IntegerField()
    fpd = models.IntegerField()
