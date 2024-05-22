from django.db import models


class Language(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class AppData(models.Model):
    name = models.CharField(max_length=255)
    release_year = models.CharField(max_length=30, null=True)  # Assuming release year is a 4-digit number
    # rating = models.CharField(max_length=10, null=True)
    poster = models.URLField()
    imdb_rating = models.CharField(max_length=10, null=True)
    rotten_rating = models.CharField(max_length=10, null=True)
    audience = models.CharField(max_length=10, null=True)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    duration = models.CharField(max_length=255, null=True)
    status_released = models.CharField(max_length=255, null=True)
    season_movie = models.CharField(max_length=10, null=True)
    where_to_watch = models.URLField()
    more_like_this = models.CharField(max_length=255, null=True)
    news_and_guides = models.CharField(max_length=255, null=True, blank=True)
    # popular_actors = models.TextField(max_length=255, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    genre = models.CharField(max_length=255, null=True)
    episodes = models.CharField(max_length=255, null=True)
    casts = models.TextField()  # Assuming cast can be a long list of names
    synopsis = models.TextField()
    # top_netflix_movies = models.TextField(null=True)
    trailer = models.URLField(blank=True, null=True)
    revenue = models.CharField(max_length=255, null=True)
    producer = models.CharField(max_length=255, null=True)
    photos = models.JSONField(null=True, blank=True)
    approval_status = models.CharField(max_length=255, null=True)
    film_studio = models.CharField(max_length=255, null=True)
    approx_budget = models.CharField(max_length=255, null=True)
    reviews = models.CharField(max_length=255, null=True)
    # Assuming photos is a list of URLs

    def __str__(self):
        return self.name
