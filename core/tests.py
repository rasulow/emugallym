from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User

class UserAPITests(APITestCase):
    
    def setUp(self):
        # Create a test user for login and OTP verification
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='password123'
        )
    
    def test_registration(self):
        """Test user registration"""
        url = reverse('registration')
        data = {
            'email': 'newuser@example.com',
            'password': 'password123',
            'password2': 'password123',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_login(self):
        """Test user login"""
        url = reverse('token_obtain_pair')
        data = {
            'email': 'admin@gmail.com',
            'password': 'admin',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_otp_verification(self):
        """Test OTP verification"""
        # Assuming OTP is stored in the user object for simplicity
        self.user.otp = '123456'
        self.user.save()
        
        url = reverse('verify-otp')
        data = {
            'email': 'testuser@example.com',
            'otp': '123456',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_token_refresh(self):
        url = reverse('token_refresh')
        login_data = {
            'email': 'admin@gmail.com',
            'password': 'admin',
        }
        login_response = self.client.post(reverse('token_obtain_pair'), login_data, format='json')
        refresh_token = login_response.data['refresh']
        
        # Now refresh the token
        refresh_data = {
            'refresh': refresh_token,
        }
        response = self.client.post(url, refresh_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

