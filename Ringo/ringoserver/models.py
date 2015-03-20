from django.db import models


class Picture(models.Model):
    picture = models.ImageField(upload_to='photos')


class Rect(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    height = models.IntegerField()
    width = models.IntegerField()

    picture = models.ForeignKey(Picture)