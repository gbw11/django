from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=100)
    profile = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Album(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="albums")
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, related_name="albums")
    release_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="reviews")
    content = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review({self.album_id})-{self.rating}"
