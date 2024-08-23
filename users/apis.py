# users/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
# from .models import CustomUser
from .serializers import CustomUserSerializer, TokenObtainPairSerializer
from django.contrib.auth import authenticate


class SignupView(APIView):
    """
    API view for user registration (signup).

    Allows users to create a new account by providing user details.
    On successful registration, returns the user data along with a 201 Created status.
    """
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(CustomUserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    API view for user login.

    Allows users to obtain JWT tokens by providing email and password.
    On successful authentication, returns the access and refresh tokens along with a 200 OK status.
    """
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(tokens, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    API view for user logout.

    Allows users to log out by providing a refresh token.
    The refresh token is blacklisted to invalidate it and prevent further use.
    On successful logout, returns a 205 Reset Content status.
    """
    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response(
                    {'detail': 'Logout successful'}, status=status.HTTP_205_RESET_CONTENT)
            except Exception as e:
                return Response(
                    {'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {'detail': 'Refresh token not provided'}, status=status.HTTP_400_BAD_REQUEST)
