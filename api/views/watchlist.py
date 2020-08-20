from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q, Sum
from rest_framework.views import APIView


# Misc Imports
from api.utils.pagination_config import PostLimitOffsetPagination


# Models Imports
from api.models import Movie, UserWatchlist, UserMovie

# Serializer
from api.serializer import UserMoviesListSerializer


class UserWatchlistHistory(ListAPIView):

    serializer_class = UserMoviesListSerializer
    pagination_class = PostLimitOffsetPagination

    def get_queryset(self, *args, **kwargs):
        search = self.request.GET.get("search", "")
        user = self.request.requested_by
        movie_list_query_result = UserWatchlist.objects.filter(user_id=user).order_by("-created_at")
        if search:
            return (
                UserWatchlist.objects.filter(Q(id__icontains=search) | Q(title__icontains=search))
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

            user_movie_history = UserMovie.objects.filter(user_id=user, movie_id=movie_id)

            if user_movie_history:
                response = {
                    "message": "Cannot add already watched movie to watchlist",
                    "status": status.HTTP_400_BAD_REQUEST,
                    "result": {},
                }
                return Response(response, response["status"])

            user_movie_obj = UserWatchlist.objects.filter(user_id=user, movie_id=movie_id).get_or_create(
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

