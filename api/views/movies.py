from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from rest_framework.views import APIView


# Misc Imports
from api.utils.pagination_config import PostLimitOffsetPagination
from api.utils.data_ingestion import DataIngestion


# Models Imports
from api.models import Movie

# Serializer Import
from api.serializer import MoviesListSerializer, MovieDetailSerializer


class MoviesList(ListAPIView):

    serializer_class = MoviesListSerializer
    pagination_class = PostLimitOffsetPagination

    def get_queryset(self, *args, **kwargs):
        search = self.request.GET.get("search", "")
        movie_list_query_result = Movie.objects.filter().order_by("-ratings")
        if search:
            return Movie.objects.filter(Q(id__icontains=search) | Q(title__icontains=search)).order_by("-ratings")
        return movie_list_query_result


class IngestMovie(APIView):
    @staticmethod
    def post(request):
        try:
            imdb_url = request.data.get("imdb_url", None)
            data_ingest = DataIngestion(imdb_url)
            data_ingest.fetch_movie_data()
            response = {
                "message": "Could not create entry",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "result": {},
            }
            return Response(response, response["status"])
        except Exception as e:
            print(e)
            response = {
                "message": "Something went wrong",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "result": {},
            }
            return Response(response, response["status"])


class MovieDetail(APIView):
    @staticmethod
    def get(request, movie_id):
        try:
            movie_obj = Movie.objects.filter(id=movie_id).first()
            movie_details = MovieDetailSerializer(instance=movie_obj, many=False).data
            response = {
                "message": "Could not create entry",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "result": movie_details,
            }
            return Response(response, response["status"])
        except Exception as e:
            print(e)
            response = {
                "message": "Something went wrong",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "result": {},
            }
            return Response(response, response["status"])
