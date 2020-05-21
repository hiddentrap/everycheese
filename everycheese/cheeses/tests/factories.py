from django.template.defaultfilters import slugify
import pytest
import factory
import factory.fuzzy

from ..models import Cheese
from ...users.tests.factories import UserFactory


@pytest.fixture
def cheese():
    return CheeseFactory()


class CheeseFactory(factory.django.DjangoModelFactory):
    name = factory.fuzzy.FuzzyText()
    slug = factory.lazy_attribute(lambda obj: slugify(obj.name))
    description = factory.Faker('paragraph', nb_sentences=3, variable_nb_sentences=True)
    firmness = factory.fuzzy.FuzzyChoice(
        [x[0] for x in Cheese.Firmness.choices]
    )
    country_of_origin = factory.Faker('country_code')
    creator = factory.SubFactory(UserFactory)

    class Meta:
        model = Cheese
