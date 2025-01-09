from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from core.models import Author
from django.utils.text import slugify



class AuthorCRUDTestCase(TestCase):

    def setUp(self):
        """Set up the test environment with an APIClient and initial data."""
        self.client = APIClient()
        self.author = Author.objects.create(
            fullname="John Doe",
            biography="An accomplished author.",
            order=1,
            is_active=True
        )

        # URL for author list and detail views (using reverse to get the URL)
        self.list_url = reverse('author-list')  # Ensure 'author-list' exists in your URLs
        self.detail_url = reverse('author-detail', kwargs={'slug': self.author.slug})  # Assuming pk is used in URLs

    def test_create_author(self):
        """Test the creation of an author."""
        data = {
            'fullname': 'Jane Doe',
            'biography': 'Biography of Jane Doe.',
            'order': 2,
            'is_active': True
        }
        response = self.client.post(self.list_url, data, format='json')

        # Check if the response status is 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check that the author count increased
        self.assertEqual(Author.objects.count(), 2)
        # Check if the created author's fullname matches the input
        self.assertEqual(Author.objects.last().fullname, 'Jane Doe')

    def test_read_author_list(self):
        """Test reading a list of authors."""
        response = self.client.get(self.list_url, format='json')

        # Check if the response status is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if one author is in the list (since we created only one in setUp)
        self.assertEqual(len(response.data), 1)

    def test_read_author_detail(self):
        """Test reading an author's detail."""
        response = self.client.get(self.detail_url, format='json')

        # Check if the response status is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if the fullname in the response matches the author's fullname
        self.assertEqual(response.data['fullname'], 'John Doe')

    def test_update_author(self):
        """Test updating an author's information."""
        data = {
            'fullname': 'John Doe Updated',
            'biography': 'Updated biography of John Doe.',
            'order': 3,
            'is_active': False
        }
        response = self.client.put(self.detail_url, data, format='json')

        # Check if the response status is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Refresh the author from the database and check if it is updated
        self.author.refresh_from_db()
        self.assertEqual(self.author.fullname, 'John Doe Updated')
        self.assertEqual(self.author.biography, 'Updated biography of John Doe.')
        self.assertEqual(self.author.order, 3)
        self.assertFalse(self.author.is_active)

    def test_partial_update_author(self):
        """Test partially updating an author's biography."""
        data = {
            'biography': 'Partially updated biography.'
        }
        response = self.client.patch(self.detail_url, data, format='json')

        # Check if the response status is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Refresh the author from the database and check if the biography is updated
        self.author.refresh_from_db()
        self.assertEqual(self.author.biography, 'Partially updated biography.')

    def test_delete_author(self):
        """Test deleting an author."""
        response = self.client.delete(self.detail_url, format='json')

        # Check if the response status is 204 No Content
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Check that the author count decreased
        self.assertEqual(Author.objects.count(), 0)