import pytest
from ..models import Cheese
from .factories import CheeseFactory

# Connects our tests with our database
pytestmark = pytest.mark.django_db


def test___str__():
    # When
    cheese = CheeseFactory()

    # Then
    assert cheese.__str__() == cheese.name
    assert str(cheese) == cheese.name

def test_get_absolute_url():
    # Given
    cheese = CheeseFactory()

    # When
    url = cheese.get_absolute_url()

    # Then
    assert url == f'/cheeses/{cheese.slug}/'
