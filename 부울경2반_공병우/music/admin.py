from django.contrib import admin
from .models import Album, Artist, Genre, Review

admin.site.register(Artist)
admin.site.register(Genre)
admin.site.register(Album)
admin.site.register(Review)
