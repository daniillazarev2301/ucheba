import pytest
from django.urls import reverse
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


def test_register_and_login():
    client = APIClient()
    register_response = client.post(
        reverse("register"),
        {"email": "test@example.com", "password": "secret123"},
        format="json",
    )
    assert register_response.status_code == 201

    login_response = client.post(
        reverse("login"),
        {"email": "test@example.com", "password": "secret123"},
        format="json",
    )
    assert login_response.status_code == 200
