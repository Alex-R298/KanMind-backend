"""Serializers for user authentication, registration and email checking."""

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token


def split_fullname(fullname):
    """Split a full name string into first and last name."""
    parts = fullname.split(" ", 1)
    first_name = parts[0]
    last_name = parts[1] if len(parts) > 1 else ""
    return first_name, last_name


class UserSerializer(serializers.ModelSerializer):
    """Handles user registration with fullname, email and password."""

    fullname = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'fullname', 'email', 'password', 'repeated_password']

    def validate_repeated_password(self, value):
        """Ensure password and repeated_password match."""
        if value != self.initial_data.get('password'):
            raise serializers.ValidationError("Passwords do not match.")
        return value

    def validate_email(self, value):
        """Ensure the email is not already registered."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        """Create a new user and generate an auth token."""
        validated_data.pop('repeated_password')
        first_name, last_name = split_fullname(validated_data.pop('fullname'))
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=first_name,
            last_name=last_name,
        )
        Token.objects.create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    """Validates login credentials (email and password)."""

    email = serializers.EmailField()
    password = serializers.CharField()


class EmailCheckSerializer(serializers.Serializer):
    """Validates the email field for the email-check endpoint."""

    email = serializers.EmailField()
