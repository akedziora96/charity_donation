import random

import pytest
from faker import Faker

from ..models import Category, Institution
from users.models import User

fake = Faker("pl_PL")

