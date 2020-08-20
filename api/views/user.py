from requests.api import request
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q, Sum
from rest_framework.views import APIView


# Misc Imports
from api.utils.pagination_config import PostLimitOffsetPagination
from api.utils.data_ingestion import DataIngestion


# Models Imports
from api.models import AuthUser, Movie, MovieActor, UserMovie

# Serializer
from api.serializer import UserMoviesListSerializer


class UserMovieHistory(ListAPIView):

    serializer_class = UserMoviesListSerializer
    pagination_class = PostLimitOffsetPagination

    def get_queryset(self, *args, **kwargs):
        search = self.request.GET.get("search", "")
        user = self.request.requested_by
        movie_list_query_result = UserMovie.objects.filter(user_id=user).order_by("-created_at")
        if search:
            return (
                UserMovie.objects.filter(Q(id__icontains=search) | Q(title__icontains=search))
                .filter(user_id=user)
                .order_by("-created_at")
            )
        return movie_list_query_result


class AddMovieToWatchList(APIView):
    @staticmethod
    def post(request):
        try:
            user = request.requested_by
            movie_id = request.data.get("movie_id")

            user_movie_obj = UserMovie.objects.filter(user_id=user, movie_id=movie_id).get_or_create(
                user_id=user, movie_id=movie_id
            )
            if user_movie_obj:
                response = {
                    "message": "Added to watch list",
                    "status": status.HTTP_201_CREATED,
                    "result": {"id": user_movie_obj[0].id},
                }
            else:
                response = {
                    "message": "couldnt create entry",
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "result": {},
                }
            return Response(response, response["status"])

        except:
            response = {
                "message": "Something went wrong",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "result": {},
            }
            return Response(response, response["status"])


class UserDashboardStats(APIView):
    @staticmethod
    def get(request):
        try:
            user = request.requested_by

            user_movie_history = (
                UserMovie.objects.filter(user_id=user)
                .values("movie_id", "movie__title", "movie__ratings")
                .order_by("-created_at")
            )

            user_watch_time = Movie.objects.filter(usermovie__user_id=user).aggregate(watch_time=Sum("runtime"))

            user_stats = {"watch_time": user_watch_time["watch_time"], "last_three_movies": user_movie_history[:3]}
            response = {
                "message": "User stats fetched successfully",
                "status": status.HTTP_201_CREATED,
                "result": user_stats,
            }
            return Response(response, response["status"])
        except Exception as e:
            response = {
                "message": "Something went wrong",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "result": {},
            }
            return Response(response, response["status"])
