import datetime
import random
import pytz

from faker import Faker
from charity_donation_project.settings import TIME_ZONE
from django.utils import timezone

fake = Faker("pl_PL")
TZ = pytz.timezone(TIME_ZONE)


def custom_fake_adress():
    return (fake.address()).split('\n')[0] + random.choice([' ', fake.random_letter().upper()])


def custom_fake_non_past_date():
    return fake.date_time_between(datetime.datetime.now(TZ), datetime.datetime(2100, 12, 31)).date()


def custom_fake_non_past_time(start_date):
    return fake.date_time_between(start_date, datetime.datetime(2100, 12, 31)).time()


if __name__ == '__main__':
    print(custom_fake_adress())
    print(custom_fake_non_past_date())
    print(custom_fake_non_past_time(custom_fake_non_past_date()))