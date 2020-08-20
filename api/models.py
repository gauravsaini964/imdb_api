from django.db import models

# Create your models here.


class Actor(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_field_active = models.BooleanField(default=True)

    class Meta:
        db_table = "actor"


class Director(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_field_active = models.BooleanField(default=True)

    class Meta:
        db_table = "director"


class Movie(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=500, blank=False, null=False)
    runtime = models.FloatField(default=60.0, null=False)
    ratings = models.FloatField(default=0.0, null=False)
    plot_summary = models.CharField(max_length=1000, blank=False)
    director = models.ForeignKey(Director, null=True, on_delete=models.SET_NULL)
    release_year = models.CharField(max_length=1000, blank=False)
    genre = models.CharField(max_length=1000, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_field_active = models.BooleanField(default=True)

    class Meta:
        db_table = "movie"


class MovieActor(models.Model):

    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_field_active = models.BooleanField(default=True)

    class Meta:
        db_table = "movie_actor"
