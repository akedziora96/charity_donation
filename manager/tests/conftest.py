import os
import sys
import random

from faker import Faker
from django.test import Client
import pytest

from users.models import User
from ..models import Category, Institution, Donation

fake = Faker("pl_PL")


@pytest.fixture
def new_user_factory():
    def create_app_user(
            username: str,
            password: str = None,
            first_name: str = "firstname",
            last_name: str = "lastname",
            email: str = "test@test.com",
            is_staff: bool = False,
            is_superuser: bool = False,
            is_active: bool = True,
    ):
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active,
        )
        return user

    return create_app_user


@pytest.fixture
def user(new_user_factory):
    return new_user_factory(username='testuser', password='testpassword')


@pytest.fixture
def inactive_user(new_user_factory):
    return new_user_factory(username='testuser', password='testpassword', is_active=False)


@pytest.fixture
def superuser(new_user_factory):
    return new_user_factory(username='testuser', password='testpassword', is_superuser=False, is_staff=False)


@pytest.fixture
def category():
    return Category.objects.create(name='testcategory')


@pytest.fixture
def institution(category):
    new_institution = Institution.objects.create(name='testinstitution', description='Lorem Ipsum', type='1')
    new_institution.categories.set(category)
    new_institution.save()
    return new_institution


@pytest.fixture
def donation(institution, user, category):
    donation = Donation.objects.create(
        quantity=10,
        institution=institution,
        address='test street 100',
        phone_number='+99 999 999 999',
        zip_code='99-999',
        pick_up_date='12-12-1212',
        pick_up_time='12:00',
        pick_up_comment='Lorem Ipsum',
        user=user
    )
    donation.categories.set(category)
    donation.save()
    return donation