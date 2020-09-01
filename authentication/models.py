from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, data):
        """Create and return a `User` with an email, username and password."""
        if data.get('email') is None:
            raise TypeError('Users must have a email.')

        user = self.model(
            email=data.get('email'),
            full_name=data.get('full_name'),
            phone_number=data.get('phone_number'),
            address=data.get('address'),
            city=data.get('city'),
            state=data.get('state'),
            country=data.get('country'),
            pin_code=data.get('pin_code')
        )
        user.set_password(data.get('password'))
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(db_index=True, unique=True)

    full_name = models.CharField(max_length=100)
    phone_number = models.IntegerField()
    address = models.CharField(max_length=1000, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    pin_code = models.IntegerField()
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    def __str__(self):
        """
        Returns a string representation of this `User`.

        This string is used when a `User` is printed in the console.
        """
        return self.email

    @property
    def token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 1 days into the future.
        """
        dt = datetime.now() + timedelta(days=settings.JWT_AUTH.get('TOKEN_EXPIRY'))

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.JWT_AUTH.get('JWT_PRIVATE_KEY'), algorithm='RS256')
        return token.decode('utf-8')
