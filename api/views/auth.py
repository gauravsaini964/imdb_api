from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password

# Misc Imports
from rest_framework_jwt.authentication import api_settings
from api.utils.jwt_generate import jwt_payload_handler
import datetime

# Models Imports
from api.models import AuthUser

JWT_ENCODER = api_settings.JWT_ENCODE_HANDLER


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


class LoginView(APIView):
    @staticmethod
    def post(request):
        try:
            email = request.data.get("email", None)
            password = request.data.get("password", None)

            user_obj = AuthUser.objects.filter(email=email).first()
            if check_password(password, user_obj.password):
                user_detail = {
                    "name": f"{user_obj.first_name} {user_obj.last_name}",
                    "email": user_obj.email,
                    "id": user_obj.id,
                    "token": JWT_ENCODER(jwt_payload_handler(user_obj)),
                }
                response = {
                    "message": "Login successful",
                    "status": status.HTTP_200_OK,
                    "result": user_detail,
                }
                return Response(response, response["status"])

            else:
                response = {
                    "message": "User does not exists",
                    "status": status.HTTP_401_UNAUTHORIZED,
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

