import pytest
from ..models import Cheese

# Connects our tests with our database
pytestmark = pytest.mark.django_db


def test___str__():
    # Given
    cheese = Cheese.objects.create(
        name="Stracchino",
        description="Semi=sweet cheese that goes well with starches.",
        firmness=Cheese.Firmness.SOFT,
    )

    # When - Then
    assert cheese.__str__() == "Stracchino"
    assert str(cheese) == "Stracchino"
