from django.test import RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from accounts.views import registerUser
from mixer.backend.django import mixer
import pytest


@pytest.fixture(scope='module')
def factory():
    return RequestFactory()


def test_authenticated_user_only_register(factory, db):
    path = reverse('register')
    request = factory.get(path)
    request.user = mixer.blend(User)
    response = registerUser(request)
    assert '/' in response.url


def test_unauthenticated_user_trying_to_register(factory, db):
    path = reverse('register')
    request = factory.get(path)
    request.user = AnonymousUser()
    response = registerUser(request)
    assert response.status_code == 200
