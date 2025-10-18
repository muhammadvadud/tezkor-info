# import pytest
# from rest_framework.test import APIClient
# from django.urls import reverse
# from django.contrib.auth import get_user_model
# from core.apps.main.models import AdModel
#
#
# @pytest.fixture
# def user(db):
#     User = get_user_model()
#     return User.objects.create_user(
#         phone="998901234567",
#         password="password123",
#         first_name="Tester",
#         last_name="User",
#     )
#
#
# @pytest.fixture
# def instance(db):
#     return AdModel._baker()
#
#
# @pytest.fixture
# def api_client(user):
#     client = APIClient()
#     # Faqat ro‘yxatdan o‘tgan user sifatida autentifikatsiya qilamiz
#     client.force_authenticate(user=user)
#     return client
#
#
# @pytest.fixture
# def data(api_client, instance):
#     return (
#         {
#             "list": reverse("ad-list"),
#             "retrieve": reverse("ad-detail", kwargs={"pk": instance.pk}),
#             "retrieve-not-found": reverse("ad-detail", kwargs={"pk": 1000}),
#         },
#         api_client,
#         instance,
#     )
#
#
# @pytest.mark.django_db
# def test_list(data):
#     urls, client, _ = data
#     response = client.get(urls["list"])
#     assert response.status_code == 200, response.json()
#     assert response.json()["status"] is True
#
#
# @pytest.mark.django_db
# def test_retrieve(data):
#     urls, client, _ = data
#     response = client.get(urls["retrieve"])
#     assert response.status_code == 200, response.json()
#     assert response.json()["status"] is True
#
#
# @pytest.mark.django_db
# def test_retrieve_not_found(data):
#     urls, client, _ = data
#     response = client.get(urls["retrieve-not-found"])
#     assert response.status_code == 404, response.json()
#     assert response.json()["status"] is False
