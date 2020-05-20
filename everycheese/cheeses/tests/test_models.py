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
