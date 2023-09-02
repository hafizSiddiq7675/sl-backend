# pylint: disable=duplicate-code
import logging
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import LoginSerializer, UserWithTokenSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


logger = logging.getLogger(__name__)
UserModel = get_user_model()


class UserLoginView(APIView):
    """
    Login and send token
    """

    permission_classes = [AllowAny]

    def post(self, request):
        # parse request
        request_serializer = LoginSerializer(data=request.data)

        # make sure request data is valid
        if not request_serializer.is_valid():
            return Response(
                {
                    'success': False,
                    'message': 'Request is invalid.',
                    'code': 'request_invalid',
                    'status': status.HTTP_400_BAD_REQUEST,
                    'data': request_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # find user by email
        request_username = request_serializer.validated_data['username']
        try:
            user = UserModel.objects.get(username=request_username.lower())
        except UserModel.DoesNotExist:
            logger.info(
                'login attempt with non-existing username: %s',
                request_username,
            )
            return Response(
                {
                    'success': False,
                    'message': 'Bad credentials.',
                    'code': 'bad_credentials',
                    'status': status.HTTP_401_UNAUTHORIZED,
                    'data': {},
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # validate user password
        if not user.check_password(
            request_serializer.validated_data['password']
        ):
            logger.info(
                'login attempt with bad password for email: %s',
                request_username,
            )
            return Response(
                {
                    'success': False,
                    'message': 'Bad credentials.',
                    'code': 'bad_credentials',
                    'status': status.HTTP_401_UNAUTHORIZED,
                    'data': {},
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # create new token or get existing one for user (will be related to
        # the user instance)
        Token.objects.get_or_create(user=user)

        # respond with user data and token
        response_serializer = UserWithTokenSerializer(user)
        return Response(
            {
                'success': True,
                'message': 'User logged in successfully.',
                'status': status.HTTP_200_OK,
                'data': response_serializer.data,
            },
            status=status.HTTP_200_OK,
        )
