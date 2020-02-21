from django.db import models


# Create your models here.
class Review(models.Model):
    user_id = models.IntegerField(null=False)
    movie_id = models.IntegerField(null=False)
    rating = models.FloatField(default=0)
    content = models.TextField(null=True, default=None)

    class Meta:
        unique_together = ['user_id', 'movie_id']
