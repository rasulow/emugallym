from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from core.models import Book, Author, Genre
from django.core.files.uploadedfile import SimpleUploadedFile

class BookCRUDTestCase(APITestCase):

    def setUp(self):
        """Set up the test environment with an APIClient and initial data."""
        self.client = APIClient()

        self.author1 = Author.objects.create(fullname="Author 1", biography="Bio 1", slug="author-1")
        self.author2 = Author.objects.create(fullname="Author 2", biography="Bio 2", slug="author-2")
        
        self.genre = Genre.objects.create(title="Fiction", slug="fiction", is_active=True)

        self.mock_file = SimpleUploadedFile("Rich-Dad-Poor-Dad.epub", b"dummy content", content_type="application/epub+zip")
        self.mock_cover = SimpleUploadedFile("rich-dad-poor-dad-9.jpg", b"dummy content", content_type="image/jpeg")

        self.book_data = {
            'title': 'Test Book',
            'description': 'This is a test book description.',
            'author': [self.author1.id, self.author2.id],
            'genre': self.genre.id,
            'price': 20.0,
            'discount': 10,
            'published_at': '2025-01-01',
            'order': 1,
            'is_active': True
        }

        self.book = Book.objects.create(
            title='Test Book',
            description='A great book.',
            price=20.0,
            slug='test-book',
            genre=self.genre,
            is_active=True
        )
        self.book.author.set([self.author1, self.author2])
        self.book.cover = self.mock_cover
        self.book.file = self.mock_file
        self.book.save()

        self.list_url = reverse('book-list') 
        self.detail_url = reverse('book-detail', kwargs={'slug': self.book.slug})

    def test_create_book(self):
        """Test the creation of a book."""
        response = self.client.post(self.list_url, self.book_data, format='multipart')

        print(response.content)
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)

        new_book = Book.objects.last()
        self.assertEqual(new_book.title, 'Test Book')
        self.assertEqual(new_book.price, 20.0)
        self.assertEqual(new_book.discount, 0)
        self.assertTrue(new_book.is_active)

    def test_get_book_detail(self):
        """Test retrieving the details of a book."""
        response = self.client.get(self.detail_url)

        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book.title)
        self.assertEqual(response.data['slug'], self.book.slug)

    def test_update_book(self):
        """Test updating a book's details."""
        updated_data = self.book_data.copy()
        updated_data['title'] = "Updated Test Book"
        updated_data['price'] = 25.00
        updated_data['discount'] = 15
        updated_data['is_active'] = False

        response = self.client.put(self.detail_url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_book = Book.objects.get(slug=self.book.slug)
        self.assertEqual(updated_book.title, "Updated Test Book")
        self.assertEqual(updated_book.price, 25.00)
        self.assertEqual(updated_book.discount, 15)
        self.assertFalse(updated_book.is_active)

    # def test_delete_book(self):
    #     """Test deleting a book."""
    #     response = self.client.delete(self.detail_url)

    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(Book.objects.count(), 1)  # Only one book should remain
    #     self.assertRaises(Book.DoesNotExist, Book.objects.get, slug=self.book.slug)
