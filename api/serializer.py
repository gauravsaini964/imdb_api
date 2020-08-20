from rest_framework import serializers
from api.models import Director, Movie, MovieActor, Actor


class MoviesListSerializer(serializers.ModelSerializer):
    cast_list = serializers.SerializerMethodField()
    director = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = (
            "id",
            "title",
            "runtime",
            "ratings",
            "plot_summary",
            "director",
            "release_year",
            "genre",
            "cast_list",
        )

    @staticmethod
    def get_cast_list(obj):
        actor_list = Actor.objects.filter(movieactor__movie_id=obj.id).values("first_name", "last_name")
        return actor_list[:3]

    @staticmethod
    def get_director(obj):
        return f"{obj.director.first_name} {obj.director.last_name}"


class MovieDetailSerializer(serializers.ModelSerializer):
    cast_list = serializers.SerializerMethodField()
    director = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = (
            "id",
            "title",
            "runtime",
            "ratings",
            "plot_summary",
            "director",
            "release_year",
            "genre",
            "cast_list",
            "plot",
        )

    @staticmethod
    def get_cast_list(obj):
        actor_list = Actor.objects.filter(movieactor__movie_id=obj.id).values("first_name", "last_name")
        return actor_list

    @staticmethod
    def get_director(obj):
        return f"{obj.director.first_name} {obj.director.last_name}"
