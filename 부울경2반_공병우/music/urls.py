from django.urls import path
from . import views

urlpatterns = [
    path("albums/", views.albums),
    path("albums/<int:pk>/", views.album_detail),
    path("albums/<int:pk>/reviews/", views.album_reviews_create),
    path("artists/<int:artist_id>/", views.artist_detail),
    path("genres/<int:genre_id>/", views.genre_detail),
]
