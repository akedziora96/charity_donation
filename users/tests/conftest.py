import os
import sys
import random

from faker import Faker
from django.test import Client
import pytest

from users.models import User


fake = Faker("pl_PL")


@pytest.fixture
def new_user_factory():
    def create_app_user(
            email: str,
            password: str = 'testpassword',
            first_name: str = "firstname",
            last_name: str = "lastname",
            is_staff: bool = False,
            is_superuser: bool = False,
            is_active: bool = True,
    ):
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active,
        )
        return user

    return create_app_user


@pytest.fixture
def user(new_user_factory):
    return new_user_factory(email='user@test.pl')


@pytest.fixture
def inacitve_user(new_user_factory):
    return new_user_factory(email='inactive_user@test.pl', is_active=False)