"""
Tests for core app
"""

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import User, Role, ContactMessage, Category, Tag


class UserModelTest(TestCase):
    """Test User model"""
    
    def setUp(self):
        self.role = Role.objects.create(name=Role.USER, description='Test user')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_user_creation(self):
        """Test user creation"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpass123'))
    
    def test_user_is_admin(self):
        """Test is_admin method"""
        self.assertFalse(self.user.is_admin())
        
        admin_role = Role.objects.create(name=Role.ADMIN)
        self.user.role = admin_role
        self.user.save()
        self.assertTrue(self.user.is_admin())
    
    def test_user_is_scholar(self):
        """Test is_scholar method"""
        self.assertFalse(self.user.is_scholar())
        
        scholar_role = Role.objects.create(name=Role.SCHOLAR)
        self.user.role = scholar_role
        self.user.save()
        self.assertTrue(self.user.is_scholar())


class UserAPITest(APITestCase):
    """Test User API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.role = Role.objects.create(name=Role.USER)
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.user.role = self.role
        self.user.save()
    
    def test_user_registration(self):
        """Test user registration"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'password2': 'newpass123'
        }
        response = self.client.post(reverse('user-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_user_registration_password_mismatch(self):
        """Test user registration with mismatched passwords"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'password2': 'differentpass123'
        }
        response = self.client.post(reverse('user-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_get_current_user(self):
        """Test getting current user profile"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('user-me'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')


class ContactMessageAPITest(APITestCase):
    """Test ContactMessage API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
    
    def test_contact_message_creation(self):
        """Test contact message submission"""
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '+996555123456',
            'subject': 'Test Subject',
            'message': 'Test message'
        }
        response = self.client.post(reverse('contact-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContactMessage.objects.count(), 1)
    
    def test_contact_message_list_unauthorized(self):
        """Test contact messages list without auth"""
        response = self.client.get(reverse('contact-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_contact_message_list_admin(self):
        """Test contact messages list with admin auth"""
        ContactMessage.objects.create(
            name='Test',
            email='test@example.com',
            subject='Test',
            message='Test message'
        )
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(reverse('contact-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CategoryAPITest(APITestCase):
    """Test Category API endpoints"""
    
    def setUp(self):
        self.category = Category.objects.create(
            name='Жаңылыктар',
            slug='news'
        )
    
    def test_category_list(self):
        """Test category list"""
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_category_retrieve(self):
        """Test category retrieve"""
        response = self.client.get(reverse('category-detail', args=[self.category.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Жаңылыктар')


class TagAPITest(APITestCase):
    """Test Tag API endpoints"""
    
    def setUp(self):
        self.tag = Tag.objects.create(
            name='исламий',
            slug='islamic'
        )
    
    def test_tag_list(self):
        """Test tag list"""
        response = self.client.get(reverse('tag-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_tag_retrieve(self):
        """Test tag retrieve"""
        response = self.client.get(reverse('tag-detail', args=[self.tag.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'исламий')
