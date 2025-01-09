from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from core.models import Genre


class GenreCRUDTestCase(TestCase):

    def setUp(self):
        """Set up the test environment with an APIClient and initial data."""
        self.client = APIClient()
        
        # Create a root genre and a child genre
        self.parent_genre = Genre.objects.create(
            title="Fiction",
            order=1,
            slug="fiction",
            is_active=True
        )
        self.child_genre = Genre.objects.create(
            title="Science Fiction",
            parent=self.parent_genre,
            order=2,
            slug="science-fiction",
            is_active=True
        )

        # URL for genre list and detail views
        self.list_url = reverse('genre-list')  # Assuming 'genre-list' from router
        self.detail_url = reverse('genre-detail', kwargs={'slug': self.parent_genre.slug})  # Assuming 'genre-detail'

    def test_create_genre(self):
        """Test the creation of a genre."""
        data = {
            'title': 'Mystery',
            'order': 3,
            'is_active': True
        }
        response = self.client.post(self.list_url, data, format='json')

        # Check if the response status is 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check that the genre count increased
        self.assertEqual(Genre.objects.count(), 3)
        # Check if the created genre's
