import pytest
from rest_framework import status
from rest_framework.test import APIClient

client = APIClient()


@pytest.mark.django_db
class TestCategoryAPI:
    def test_post_category(self):
        payload = dict(
            title="string",
            is_active=True,
            order=1,
        )

        response = client.post('/api/category/', data=payload, format='json')

        data = response.data
        print(data)

        assert response.status_code == status.HTTP_201_CREATED
        assert data['title'] == payload['title']
        assert data['is_active'] == payload['is_active']
        assert data['order'] == payload['order']
        assert 'slug' in data
        assert data['slug'] != ''

    def test_get_category(self):
        response = client.get('/api/category/')
        data = response.data
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(data, list)
