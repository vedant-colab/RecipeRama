from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from recipe.models import Contact
from userauth.models import CustomUser

class RecipeTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_recommend_view_authenticated(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('recommend'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recommend.html')

    def test_recommend_view_unauthenticated(self):
        response = self.client.get(reverse('recommend'))
        self.assertEqual(response.status_code, 302)  # Redirects to login page for unauthenticated user

    def test_recommend_post_view(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(reverse('recommend'), {
            'recipeName': 'Test Recipe',
            'numRecipes': 5
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recommend.html')
        self.assertContains(response, 'Test Recipe')

    def test_contact_view(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')

    def test_contact_post_view(self):
        response = self.client.post(reverse('contact'), {
            'name': 'Test Name',
            'email': 'test@example.com',
            'msg': 'Test Message'
        })
        self.assertEqual(response.status_code, 200)  # Assuming the contact view renders a template after form submission

        # Check if the contact form data is saved
        contact_entry = Contact.objects.get(name='Test Name')
        self.assertEqual(contact_entry.email, 'test@example.com')
        self.assertEqual(contact_entry.msg, 'Test Message')

    def test_about_view(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')