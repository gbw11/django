from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Album, Artist, Genre
from .serializers import (
    AlbumCreateUpdateSerializer,
    AlbumDetailSerializer,
    AlbumListSerializer,
    ArtistDetailSerializer,
    ReviewSerializer,
    GenreSerializer,
)


@api_view(["GET", "POST"])
def albums(request):
    if request.method == "GET":
        queryset = Album.objects.select_related("artist").all()
        serializer = AlbumListSerializer(queryset, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = AlbumCreateUpdateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            album = serializer.save()
            detail = AlbumDetailSerializer(album)
            return Response(detail.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
def album_detail(request, pk):
    album = get_object_or_404(Album.objects.select_related("artist", "genre").prefetch_related("reviews"), pk=pk)

    if request.method == "GET":
        serializer = AlbumDetailSerializer(album)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = AlbumCreateUpdateSerializer(album, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            serializer = AlbumDetailSerializer(album)
            return Response(serializer.data)

    if request.method == "DELETE":
        album.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def album_reviews_create(request, pk):
    if request.method == "POST":
        album = get_object_or_404(Album.objects, pk=pk)
        serializer = ReviewSerializer(data=request.data)
        if request.data["rating"]<1 or request.data["rating"]>5:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save(album=album)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def artist_detail(request, artist_id):
    artist = get_object_or_404(Artist.objects, pk=artist_id)
    serializer = ArtistDetailSerializer(artist, data=request.data)
    return Response(serializer.data)


@api_view(["GET"])
def genre_detail(request, genre_id):
    genre = get_object_or_404(Genre.objects, pk=genre_id)
    serializer = GenreSerializer(genre, data=request.data)
    return Response(serializer.data)
