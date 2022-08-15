import pytest
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from faker import Faker

from ..models import User
from ..utils import account_activation_token

fake = Faker("pl_PL")


@pytest.mark.django_db
def test_login_view(client, new_user_factory):
    url = reverse('login')
    redirect_url = reverse('landing-page')

    new_password = 'testpassword'
    user = new_user_factory(email='new_user@test.pl', password=new_password)

    response = client.get(url)
    assert response.status_code == 200

    post_response = client.post(url, {'username': user.email, 'password': new_password})
    assert post_response.status_code == 302
    assert post_response.url == redirect_url


@pytest.mark.django_db
def test_login_view_with_invalid_data(client):
    url = reverse('login')

    response = client.get(url)
    assert response.status_code == 200

    post_response = client.post(url, {})
    assert post_response.status_code == 200


@pytest.mark.django_db
def test_login_view_with_already_loged_user(client, user):
    url = reverse('login')
    redirect_url = reverse('landing-page')
    client.force_login(user)

    response = client.get(url)
    assert response.status_code == 302
    assert response.url == redirect_url

    post_response = client.post(url, {})
    assert post_response.status_code == 302
    assert post_response.url == redirect_url


@pytest.mark.django_db
def test_loggout_view_loged_user(client, user):
    url = reverse('logout-page')
    redirect_url = reverse('landing-page')
    client.force_login(user)

    response = client.get(url)
    assert response.status_code == 302
    assert response.url == redirect_url

    post_response = client.post(url, {})
    assert post_response.status_code == 302
    assert post_response.url == redirect_url


@pytest.mark.django_db
def test_loggout_view_non_loged_user(client, user):
    url = reverse('logout-page')
    redirect_url = reverse('landing-page')
    client.logout()

    response = client.get(url)
    assert response.status_code == 302
    assert response.url == redirect_url

    post_response = client.post(url, {})
    assert post_response.status_code == 302
    assert post_response.url == redirect_url


@pytest.mark.django_db
def test_register_view(client):
    url = reverse('register')
    redirect_url = reverse('login')

    user_count_before_create = User.objects.count()

    response = client.get(url)
    assert response.status_code == 200

    data = {
        'email': fake.email(),
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'password1': 'superstrongpassword12345',
        'password2': 'superstrongpassword12345',
    }

    post_response = client.post(url, data)

    assert post_response.status_code == 302
    assert post_response.url == redirect_url
    user_count_after_create = User.objects.count()

    assert user_count_after_create == user_count_before_create + 1


@pytest.mark.django_db
def test_register_view_logged_user(client, user):
    url = reverse('register')
    redirect_url = reverse('landing-page')
    client.force_login(user)

    response = client.get(url)
    assert response.status_code == 302
    assert response.url == redirect_url


@pytest.mark.django_db
def test_user_activate_view_non_logged_user(client, inacitve_user):
    uid = urlsafe_base64_encode(force_bytes(inacitve_user.pk))
    token = account_activation_token.make_token(inacitve_user)

    url = reverse('activate', args=[uid, token])

    assert inacitve_user.is_active is False

    response = client.get(url)
    assert response.status_code == 200
    assert response.context['status'] == 'user is now activated'

    activated_user = User.objects.get(id=inacitve_user.id)
    assert activated_user.is_active is True


@pytest.mark.django_db
def test_user_detail_view(client, user, donation):
    url = reverse('user-details')
    client.force_login(user)

    response = client.get(url)
    assert response.status_code == 200
    assert list(response.context['object_list']) == list(user.donation_set.all())


@pytest.mark.django_db
def test_user_edit_view(client, user):
    url = reverse('user-edit')
    redirect_url = reverse('landing-page')
    client.force_login(user)

    response = client.get(url)
    assert response.status_code == 200

    data = {
        'email': fake.email(),
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
    }

    post_response = client.post(url, data)

    assert post_response.status_code == 302
    assert post_response.url == redirect_url

    user = User.objects.get(id=user.id)
    assert user.email == data['email']
    assert user.first_name == data['first_name']
    assert user.last_name == data['last_name']


@pytest.mark.django_db
def test_user_password_change_view(client, new_user_factory):
    url = reverse('password_change')
    redirect_url = reverse('password_change_done')

    current_password = 'testpassword'
    user = new_user_factory(email='new_user@test.pl', password=current_password)

    client.force_login(user)

    response = client.get(url)
    assert response.status_code == 200

    data = {
        'old_password': current_password,
        'new_password1': 'superstrongpassword12345',
        'new_password2': 'superstrongpassword12345'
    }

    post_response = client.post(url, data)

    assert post_response.status_code == 302
    assert post_response.url == redirect_url

    client.login(username=user.email, password=data['new_password1'])
    response = client.get(reverse('login'))

    assert response.status_code == 302
    assert response.url == reverse('landing-page')


@pytest.mark.django_db
def test_user_password_reset_view(client, user):
    url = reverse('password_reset')
    redirect_url = reverse('password_reset_done')

    response = client.get(url)
    assert response.status_code == 200

    data = {
        'email': user.email,
    }

    post_response = client.post(url, data)

    assert post_response.status_code == 302
    assert post_response.url == redirect_url


@pytest.mark.django_db
def test_user_password_reset_confirm_view(client, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)

    url = reverse('password_reset_confirm', args=[uid, token])
    redirect_url = reverse('password_reset_complete')

    response = client.get(url)
    assert response.status_code == 200

    data = {
        'new_password1': 'superstrongpassword12345',
        'new_password2': 'superstrongpassword12345',
    }

    post_response = client.post(url, data)

    assert post_response.status_code == 302
    assert post_response.url == redirect_url