from faker import Faker
import pytest

from manager.models import Donation, Category, Institution
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


@pytest.fixture
def category():
    return Category.objects.create(name='testcategory')


@pytest.fixture
def foundation(category):
    new_foundation = Institution.objects.create(name='testfoundation', description='Lorem Ipsum', type='1')
    new_foundation.categories.add(category)
    new_foundation.save()
    return new_foundation


@pytest.fixture
def donation(foundation, user, category):
    donation = Donation.objects.create(
        quantity=10,
        institution=foundation,
        address='test street 100',
        phone_number='+99 999 999 999',
        zip_code='99-999',
        pick_up_date='2012-12-12',
        pick_up_time='12:00:00',
        pick_up_comment='Lorem Ipsum',
        user=user
    )
    donation.categories.add(category)
    donation.save()
    return donation