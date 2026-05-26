from rest_framework import serializers
from .models import Album, Artist, Genre, Review


class ArtistBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = "__all__"


class ArtistDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ["id", "name"]





class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "content", "rating"]


class AlbumListSerializer(serializers.ModelSerializer):
    artist = ArtistDetailSerializer(read_only=True)

    class Meta:
        model = Album
        fields = [
            'id',
            'title',
            'artist'
        ]

class GenreSerializer(serializers.ModelSerializer):
    albums = AlbumListSerializer(read_only=True)
    class Meta:
        model = Genre
        fields = ["id", "name", 'albums']

class AlbumDetailSerializer(serializers.ModelSerializer):
    artist = ArtistBasicSerializer(read_only=True)
    genre = GenreSerializer(read_only=True)
    reviews = ReviewSerializer(read_only=True, many=True)
    class Meta:
        model = Album
        fields = ["id", "title", "artist", "genre", "release_date",
                  "description", "reviews"]


class AlbumCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ["title", "artist", "genre", "release_date", "description"]

