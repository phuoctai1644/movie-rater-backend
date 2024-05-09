import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator


def get_upload_path(instance, file_name):
    return os.path.join('thumbnail', str(instance.pk), file_name)


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars', blank=True)

    def __str__(self):
        return self.username


class Movie(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=1080)
    year = models.PositiveIntegerField(validators=[MinValueValidator(1900)], blank=True)
    thumbnail = models.ImageField(upload_to=get_upload_path, blank=True, null=True)
    type = models.CharField(max_length=128, blank=True)
    trailer_url = models.CharField(max_length=512, blank=True)

    def __str__(self):
        return self.title

    def total_rating(self):
        ratings = Rating.objects.filter(movie=self)
        return len(ratings)

    def avg_rating(self):
        total = 0
        ratings = Rating.objects.filter(movie=self)
        for rating in ratings:
            total += rating.stars

        if total > 0:
            return total / len(ratings)
        else:
            return 0


class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    description = models.TextField(max_length=1080)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('movie', 'user'),)
        index_together = (('movie', 'user'),)
