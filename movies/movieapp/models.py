from django.db import models
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=50)
    release_year = models.PositiveIntegerField(null=False)
    director = models.CharField(max_length=50)
    writer = models.CharField(max_length=50, default="")
    genre = models.CharField(max_length=50)
    description = models.TextField(default="")
    country = models.CharField(max_length=50)
    rating = models.FloatField(default=0)
    box_office = models.IntegerField()


class Feature(models.Model):
    title = models.CharField(max_length=100)


class MovieFeature(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    description = models.TextField(default="")


class MovieInfo(models.Model):
    title = models.CharField(max_length=50)
    release_year = models.PositiveIntegerField(null=False)
    director = models.CharField(max_length=50)
    writer = models.CharField(max_length=50, default="")
    genre = models.CharField(max_length=50)
    description = models.TextField(default="")
    country = models.CharField(max_length=50)
    rating = models.FloatField(default=0)
    box_office = models.IntegerField()
    feature_name = ArrayField(models.CharField(max_length=50))
    feature_description = ArrayField(models.TextField(default=""))
    class Meta:
        managed = False
        db_table = 'movieapp_movieinfo'
