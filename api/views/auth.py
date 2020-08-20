from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password

# Misc Imports
import bcrypt
from api.utils.jwt_generate import jwt_payload_handler

# Models Imports
from api.models import AuthUser


class RegisterView(APIView):
    @staticmethod
    def post(request):
        try:
            name = request.data.get("name", None)
            email = request.data.get("email", None)
            password = request.data.get("password", None)
            hashed_pass = make_password(password)
            print(hashed_pass)
            response = {
                "message": "Something went wrong",
                "status": status.HTTP_201_CREATED,
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

