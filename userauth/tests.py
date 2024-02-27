from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile, CustomUser
from blog.models import Blog

class UserAuthTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def test_signup_view(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword'
        })
        self.assertEqual(response.status_code, 302)  # Check if the user is redirected after successful signup
        self.assertRedirects(response, reverse('dashboard'))

    def test_signin_view(self):
        response = self.client.post(reverse('signin'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)  # Check if the user is redirected after successful login
        self.assertRedirects(response, reverse('dashboard'))

    def test_dashboard_view(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)  # Check if the dashboard page returns a successful response

    def test_edit_profile_view(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)  # Check if the edit profile page returns a successful response

        # Test profile editing (POST request)
        response = self.client.post(reverse('edit_profile'), {
            'name': 'New Name',
            'bio': 'New Bio',
            'location': 'New Location',
            'dob': '1990-01-01'
        })
        self.assertEqual(response.status_code, 302)  # Check if the user is redirected after profile edit
        self.assertRedirects(response, reverse('view_profile'))

        # Check if the profile details are updated
        updated_profile = Profile.objects.get(user=self.user)
        self.assertEqual(updated_profile.name, 'New Name')
        self.assertEqual(updated_profile.bio, 'New Bio')
        self.assertEqual(updated_profile.country, 'New Location')
        self.assertEqual(str(updated_profile.dob), '1990-01-01')

    def test_view_profile_view(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('view_profile'))
        self.assertEqual(response.status_code, 200)  # Check if the view profile page returns a successful response

    def test_view_blogs_view(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('view_blogs'))
        self.assertEqual(response.status_code, 200)  # Check if the view blogs page returns a successful response


