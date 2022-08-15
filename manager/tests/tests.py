import random

import pytest
from django.urls import reverse
from faker import Faker

from .utils import custom_fake_adress, custom_fake_non_past_date, custom_fake_non_past_time
from ..models import Institution, Donation

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
    assert response.url == reverse('login') + '?next=' + url

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
def test_pagination_api_view_foundation(client, foundation):
    url = reverse('pagination-api') + f'?page=1&type={foundation.type}'
    response = client.get(url)
    responseJson = response.json()
    assert response.status_code == 200
    assert responseJson[0]['pk'] == foundation.id
    assert response.status_code == 200
    assert responseJson[0]['pk'] == foundation.id
    assert responseJson[0]['fields']['name'] == foundation.name
    assert responseJson[0]['fields']['type'] == int(foundation.type)
    assert responseJson[0]['fields']['description'] == foundation.description


@pytest.mark.django_db
def test_pagination_api_view_ngo(client, ngo):
    url = reverse('pagination-api') + f'?page=1&type={ngo.type}'
    response = client.get(url)
    responseJson = response.json()
    assert response.status_code == 200
    assert responseJson[0]['pk'] == ngo.id
    assert response.status_code == 200
    assert responseJson[0]['pk'] == ngo.id
    assert responseJson[0]['fields']['name'] == ngo.name
    assert responseJson[0]['fields']['type'] == int(ngo.type)
    assert responseJson[0]['fields']['description'] == ngo.description


@pytest.mark.django_db
def test_pagination_api_view_collection(client, collection):
    url = reverse('pagination-api') + f'?page=1&type={collection.type}'
    response = client.get(url)
    responseJson = response.json()
    assert response.status_code == 200
    assert responseJson[0]['pk'] == collection.id
    assert response.status_code == 200
    assert responseJson[0]['pk'] == collection.id
    assert responseJson[0]['fields']['name'] == collection.name
    assert responseJson[0]['fields']['type'] == int(collection.type)
    assert responseJson[0]['fields']['description'] == collection.description


@pytest.mark.django_db
def test_get_donation_api_view_non_loged_users(client, donation):
    url = reverse('donation-api')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('login') + '?next=' + url


@pytest.mark.django_db
def test_get_donation_api_view_loged_users_donation_untaken(client, donation, user):
    url = reverse('donation-api') + f'?id={donation.id}'
    client.force_login(user)

    donation.is_taken = False
    donation.save()
    assert donation.is_taken is False

    response = client.get(url)
    responseJson = response.json()
    assert response.status_code == 200
    assert responseJson[0]['pk'] == donation.id
    assert responseJson[0]['fields']['quantity'] == donation.quantity

    institution = Institution.objects.get(id=donation.institution.id)
    assert responseJson[0]['fields']['institution'] == institution.natural_key()

    assert responseJson[0]['fields']['address'] == donation.address
    assert responseJson[0]['fields']['phone_number'] == donation.phone_number
    assert responseJson[0]['fields']['zip_code'] == donation.zip_code
    assert responseJson[0]['fields']['pick_up_date'] == donation.pick_up_date
    assert responseJson[0]['fields']['pick_up_time'] == donation.pick_up_time
    assert responseJson[0]['fields']['pick_up_comment'] == donation.pick_up_comment
    assert responseJson[0]['fields']['user'][0] == user.email
    assert responseJson[0]['fields']['is_taken'] is True


@pytest.mark.django_db
def test_get_donation_api_view_loged_users_donation_taken(client, donation, user):
    url = reverse('donation-api') + f'?id={donation.id}'
    client.force_login(user)

    donation.is_taken = True
    donation.save()
    assert donation.is_taken is True

    response = client.get(url)
    responseJson = response.json()
    assert response.status_code == 200
    assert responseJson[0]['pk'] == donation.id
    assert responseJson[0]['fields']['is_taken'] is False


@pytest.mark.django_db
def test_get_institution_api_view_non_loged_users(client, foundation, category):
    url = reverse('institution-api')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('login') + '?next=' + url


@pytest.mark.django_db
def test_get_institution_api_view_loged_users(client, foundation, category, user):
    url = reverse('institution-api') + f'?id={category.id}'
    client.force_login(user)

    response = client.get(url)
    responseJson = response.json()
    assert response.status_code == 200
    assert responseJson[0]['pk'] == foundation.id
    assert responseJson[0]['fields']['name'] == foundation.name
    assert responseJson[0]['fields']['type'] == int(foundation.type)
    assert responseJson[0]['fields']['description'] == foundation.description
    assert responseJson[0]['fields']['categories'][0] == category.id


@pytest.mark.django_db
def test_get_institution_api_view_intersection(client, foundation, second_foundation, category, second_category, user):
    """Tests if "GET" method returns only institutions which simultaneously take gift af all chosen categories"""
    url_without_tags = reverse('institution-api')
    url_with_tags = reverse('institution-api') + f'?id={category.id}&id={second_category.id}'
    client.force_login(user)

    response = client.get(url_without_tags)
    responseJson = response.json()

    assert response.status_code == 200
    assert len(responseJson) == 2

    response = client.get(url_with_tags)
    responseJson = response.json()

    assert response.status_code == 200
    assert len(responseJson) == 1


@pytest.mark.django_db
def test_save_donation_api_view_non_loged_users(client):
    url = reverse('save-donation-api')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('login') + '?next=' + url


# @pytest.mark.repeat(1000)
@pytest.mark.django_db
def test_save_donation_api_view_loged_users(client, user, category, foundation):
    url = reverse('save-donation-api')
    client.force_login(user)

    count_before_post = Donation.objects.count()

    pick_up_date = custom_fake_non_past_date()
    pick_up_time = custom_fake_non_past_time(pick_up_date)

    data = {
        'quantity': random.randint(1, 100),
        'categories': [category.id, ],
        'institution': foundation.id,
        'address': custom_fake_adress(),
        'city': fake.city(),
        'zip_code': fake.postcode(),
        'phone_number': fake.phone_number(),
        'pick_up_date': pick_up_date,
        'pick_up_time': pick_up_time,
        'pick_up_comment': fake.text(),
    }

    response = client.post(url, data)
    responseJson = response.json()

    count_after_post = Donation.objects.count()

    assert response.status_code == 200
    assert responseJson['status'] == 'success'
    assert count_after_post == count_before_post + 1


@pytest.mark.django_db
def test_save_donation_api_view_loged_users_with_invalid_form_data(client, user):
    url = reverse('save-donation-api')
    client.force_login(user)

    data = None

    response = client.post(url, data)
    responseJson = response.json()

    assert response.status_code == 200
    assert responseJson['status'] == 'error'


@pytest.mark.django_db
def test_send_contact_mail_api_view_non_loged_users(client):
    url = reverse('contact-api')

    data = {
        'first_name': fake.first_name(),
        'last_name':  fake.last_name(),
        'email': fake.email(),
        'message': fake.text(),
    }

    response = client.post(url, data)
    responseJson = response.json()

    assert response.status_code == 200
    assert responseJson['status'] == 'success'


@pytest.mark.django_db
def test_send_contact_mail_api_view_non_loged_users_with_invalid_form_data(client):
    url = reverse('contact-api')

    data = None

    response = client.post(url, data)
    responseJson = response.json()

    assert response.status_code == 200
    assert responseJson['status'] == 'error'


@pytest.mark.django_db
def test_send_contact_mail_api_view_loged_users(client, user):
    url = reverse('contact-api')
    client.force_login(user)

    data = {'message': fake.text()}

    response = client.post(url, data)
    responseJson = response.json()

    assert response.status_code == 200
    assert responseJson['status'] == 'success'


@pytest.mark.django_db
def test_send_contact_mail_api_view_loged_users_with_invalid_form_data(client, user):
    url = reverse('contact-api')
    client.force_login(user)

    data = None

    response = client.post(url, data)
    responseJson = response.json()

    assert response.status_code == 200
    assert responseJson['status'] == 'error'