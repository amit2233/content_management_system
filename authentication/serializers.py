import re

from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from rest_framework import serializers


from .models import User

phone_regex = RegexValidator(
    regex=r'^\+?1?\d{10,10}$',
    message="Phone number must be entered in the format: '9999999999'."
)
pin_code_regex = RegexValidator(
    regex=r'^\d{6,6}$',
    message="Pincode must be in 6 digit"
)


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    password = serializers.CharField(
        min_length=8,
        write_only=True
    )
    phone_number = serializers.IntegerField(validators=[phone_regex])
    pin_code = serializers.IntegerField(validators=[pin_code_regex])

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'phone_number', 'pin_code', 'full_name', 'address', 'city', 'state',
                  'token']

    def create(self, validated_data):
        user = User.objects.create_user(validated_data)
        return user

    def validate(self, data):
        password = data.get('password')
        if not re.search(r'[A-Z]', password):
            raise serializers.ValidationError(
                'A password must contain 1 capital letter'
            )
        if not re.search(r'[a-z]', password):
            raise serializers.ValidationError(
                'A password must contain 1 small letter.'
            )
        return data


class LoginSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):

        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'A email is required to log in.'
            )

        # Raise an exception if a
        # password is not provided.
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this email/password combination. Notice how
        # we pass `email` as the `username` value since in our User
        # model we set `USERNAME_FIELD` as `email`.
        user = authenticate(email=email, password=password)

        # If no user was found matching this email/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        return {
            'id': user.id,
            'email': user.email,
            'token': user.token
        }

