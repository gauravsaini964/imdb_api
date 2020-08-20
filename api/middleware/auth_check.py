# REST Imports.
# from rest_framework.views import APIView
# from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
import jwt
from rest_framework_jwt.authentication import api_settings
from movie_watchtime.settings import API_KEY

# from rest_framework.authentication import get_authorization_header

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER

# MISC Imports.
import time
import json

# Model import
from api.models import AuthUser


class KeyAndTokenCheck:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        res = {"message": "Api Key Invalid."}
        request.start_time = time.time()
        try:
            if request.META["HTTP_KEY"]:
                auth_key = request.META["HTTP_KEY"]
                if API_KEY != auth_key:
                    return HttpResponse(json.dumps(res), status.HTTP_401_UNAUTHORIZED)
        except:
            return HttpResponse(json.dumps(res), status.HTTP_401_UNAUTHORIZED)

        try:
            if not request.path.startswith("/v1/auth/"):
                auth = request.META["HTTP_AUTHORIZATION"].split()[1]
                try:
                    payload = jwt_decode_handler(auth)
                    user_obj = AuthUser.objects.get(id=payload.get("sub"))
                    if user_obj:
                        request.requested_by = payload.get("sub")
                except AuthUser.DoesNotExist:
                    request.requested_by = None
                    return HttpResponse(
                        json.dumps({"message": "User is logged out. Login again."}), status.HTTP_401_UNAUTHORIZED
                    )
                except jwt.ExpiredSignature:
                    request.requested_by = None
                    return HttpResponse(
                        json.dumps({"message": "Signature has expired."}), status.HTTP_401_UNAUTHORIZED
                    )
                except jwt.DecodeError:
                    request.requested_by = None
                    return HttpResponse(
                        json.dumps({"message": "Error decoding signature."}), status.HTTP_401_UNAUTHORIZED
                    )
                except jwt.InvalidTokenError:
                    request.requested_by = None
                    return HttpResponse(
                        json.dumps({"message": "Incorrect authentication token."}), status.HTTP_401_UNAUTHORIZED
                    )
        except Exception as e:
            return HttpResponse(json.dumps({"error": "No Authorization token provided"}), status.HTTP_401_UNAUTHORIZED)

        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called

        return response
