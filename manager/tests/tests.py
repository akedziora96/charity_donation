import json
import random

import jsonpath as jsonpath
import pytest
from django.urls import reverse
from faker import Faker
import requests

from ..models import Category, Institution
from users.models import User

fake = Faker("pl_PL")


@pytest.mark.django_db
def test_landing_page_view(client, foundation, ngo, collection, donation):
    url = reverse('landing-page')
    response = client.get(url)
    assert response.status_code == 200
    assert list(response.context['foundations'])[0] == foundation
    assert list(response.context['ngos'])[0] == ngo
    assert list(response.context['charity_collections'])[0] == collection
    assert response.context['total_donated_quantity'].get('quantity__sum') == 10
    assert response.context['donated_institutions'] == 1


@pytest.mark.django_db
def test_donation_add_view(client, user, category):
    url = reverse('add-donation')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == f"{reverse('login')}?next={url}"

    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['categories'].count() == 1


@pytest.mark.django_db
def test_donation_confirmation_view(client, user):
    url = reverse('confirm-donation')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == f"{reverse('login')}?next={url}"

    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_contact_confirmation_view(client, user):
    url = reverse('confirm-contact')
    response = client.get(url)
    assert response.status_code == 200

    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_pagination_api_view_without_tag(client):
    url = reverse('pagination-api')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_pagination_api_view_without_tag(client):
    url = reverse('pagination-api')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_pagination_api_view_fetch_data(client):
    category = Category.objects.create(name='test')
    api_address = f'http://127.0.0.1:8000/get-institution-api/?id={category.id}'

    response = requests.get(api_address)
    responseJson = response.json()
    assert response.status_code == 200
    assert responseJson[0]['pk'] == category.id


