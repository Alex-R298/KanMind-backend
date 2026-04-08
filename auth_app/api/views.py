"""Views for user registration, login, logout and email checking."""

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import EmailCheckSerializer, LoginSerializer, UserSerializer


def get_fullname(user):
    """Return the user's full name from first_name and last_name."""
    return f"{user.first_name} {user.last_name}".strip()


def build_auth_response(user, token):
    """Build the standard auth response payload."""
    return {
        "token": token.key,
        "user_id": user.id,
        "email": user.email,
        "fullname": get_fullname(user),
    }


class RegisterView(APIView):
    """Create a new user account and return auth credentials."""

    permission_classes = [AllowAny]

    def post(self, request):
        """Handle user registration."""
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        token = Token.objects.get(user=user)
        return Response(build_auth_response(user, token), status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """Authenticate an existing user via email and password."""

    permission_classes = [AllowAny]

    def post(self, request):
        """Validate credentials and return auth token."""
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self._authenticate(serializer.validated_data)
        if user is None:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)
        token, _ = Token.objects.get_or_create(user=user)
        return Response(build_auth_response(user, token), status=status.HTTP_200_OK)

    def _authenticate(self, data):
        """Look up user by email and verify the password."""
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            return None
        return authenticate(username=user.username, password=data['password'])


class EmailCheckView(APIView):
    """Check whether an email address is already registered."""

    permission_classes = [AllowAny]

    def post(self, request):
        """Return whether the given email exists in the database."""
        serializer = EmailCheckSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        exists = User.objects.filter(email=serializer.validated_data['email']).exists()
        return Response({"exists": exists}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """Delete the user's auth token to log them out."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Remove the auth token for the current user."""
        request.user.auth_token.delete()
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
