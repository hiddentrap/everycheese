import pytest
from pytest_django.asserts import assertContains, assertRedirects

from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory

from everycheese.users.models import User
from ..models import Cheese
from ..views import (
    CheeseCreateView,
    CheeseListView,
    CheeseDetailView
)
from .factories import CheeseFactory

pytestmark = pytest.mark.django_db


def test_good_cheese_list_view_expanded(rf):
    # 사용자는 URL을 입력한다.
    url = reverse("cheeses:list")
    # rf = pytest의 django.test.RequestFactory의 레퍼런스
    # 사용자가 입력한 것처럼 리퀘스트를 만들어낸다.
    request = rf.get(url)
    # function-based view와 유사한 호출 view생성
    callable_obj = CheeseListView.as_view()

    # View에 리퀘스트를 전달하여 HTTP Response를 응답받는다.
    response = callable_obj(request)

    # HTTP 응답에 'Cheese List'가 있는지 확인한다.
    assertContains(response, 'Cheese List')


def test_cheese_list_contains_2_cheeses(rf):
    # Given
    cheese1 = CheeseFactory()
    cheese2 = CheeseFactory()
    request = rf.get(reverse("cheeses:list"))
    # When
    response = CheeseListView.as_view()(request)
    # Then
    assertContains(response, cheese1.name)
    assertContains(response, cheese2.name)


def test_good_cheese_detail_view(rf):
    # 치즈 팩토리에 치즈를 주문한다.
    cheese = CheeseFactory()
    # 치즈 정보에 대한 요청을 만든다.
    url = reverse("cheeses:detail", kwargs={'slug': cheese.slug})
    request = rf.get(url)
    # 치즈 정보를 요청한다.
    callable_obj = CheeseDetailView.as_view()
    response = callable_obj(request, slug=cheese.slug)
    # 제대로된 이름이 들어있는지를 확인한다.
    assertContains(response, cheese.name)


def test_detail_contains_cheese_data(rf):
    # Given
    cheese = CheeseFactory()
    request = rf.get(reverse("cheeses:detail", kwargs={'slug': cheese.slug}))
    # When
    response = CheeseDetailView.as_view()(request, slug=cheese.slug)
    # Then
    assertContains(response, cheese.name)
    assertContains(response, cheese.get_firmness_display())
    assertContains(response, cheese.country_of_origin.name)


def test_good_cheese_create_view(rf, admin_user):
    # 치즈를 주문한다.
    cheese = CheeseFactory()
    # 새 치즈에 대한 요청을 만든다.
    request = rf.get(reverse("cheeses:add"))
    # 사용자 인증 정보를 추가한다.
    request.user = admin_user
    # 요청을 보낸다
    response = CheeseCreateView.as_view()(request)
    # 응답 상태코드를 확인한다.
    assert response.status_code == 200

def test_cheese_create_form_valid(rf, admin_user):
    # Given
    form_data = {
        "name": "Paski Sir",
        "description": "A salty hard cheese",
        "firmness": Cheese.Firmness.HARD
    }
    request = rf.post(reverse("cheeses:add"), form_data)
    request.user = admin_user
    # When
    response = CheeseCreateView.as_view()(request)
    cheese = Cheese.objects.get(name="Paski Sir")
    # Then
    assert cheese.description == "A salty hard cheese"
    assert cheese.firmness == Cheese.Firmness.HARD
    assert cheese.creator == admin_user
