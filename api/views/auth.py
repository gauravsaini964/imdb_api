from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password

# Misc Imports
from api.utils.jwt_generate import jwt_payload_handler
import datetime

# Models Imports
from api.models import AuthUser


class RegisterView(APIView):
    @staticmethod
    def post(request):
        try:
            first_name = request.data.get("first_name", None)
            last_name = request.data.get("last_name", None)
            email = request.data.get("email", None)
            password = request.data.get("password", None)
            hashed_pass = make_password(password)
            user_name = email.split("@")[0]
            user_obj = AuthUser.objects.create(
                password=hashed_pass,
                last_login=datetime.datetime.now(),
                email=email,
                last_name=last_name,
                username=user_name,
                first_name=first_name,
            )
            if user_obj:
                user_info = {"user_id": user_obj.id}
                response = {
                    "message": "User signed up successfully",
                    "status": status.HTTP_201_CREATED,
                    "result": user_info,
                }
            else:
                response = {
                    "message": "Could not create entry",
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

