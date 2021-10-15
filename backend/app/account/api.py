from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_jwt.settings import api_settings

from .serializers import UserSerializer, RegisterSerializer, LoginSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token,
            "expired": api_settings.JWT_EXPIRATION_DELTA
        })


class LoginApi(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        return Response({
            "token": token,
            "expired": api_settings.JWT_EXPIRATION_DELTA
        })
