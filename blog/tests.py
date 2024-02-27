from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Blog
from userauth.models import Profile, CustomUser
from datetime import datetime

class BlogTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        # Create a test profile
        self.profile = Profile.objects.create(user=self.user)

        # Create a test blog post
        self.blog_post = Blog.objects.create(
            author=self.profile,
            title='Test Blog',
            content='This is a test blog post.',
            created_at=datetime.today(),
            updated_at=datetime.today(),
        )

    def test_blog_view(self):
        response = self.client.get(reverse('blog_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog.html')
        self.assertContains(response, 'Test Blog')

    def test_create_blog_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('create_blog'), {
            'title': 'New Blog',
            'content': 'This is a new blog post.'
        })
        self.assertEqual(response.status_code, 200)  # Assuming the create_blog view renders a template after creating a blog post

        # Check if the new blog post is created
        new_blog_post = Blog.objects.get(title='New Blog')
        self.assertEqual(new_blog_post.author, self.profile)

    def test_blog_detail_view(self):
        response = self.client.get(reverse('blog_detail', args=[self.blog_post.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog_detail.html')
        self.assertContains(response, 'Test Blog')

    def test_search_view(self):
        response = self.client.get(reverse('search_view') + '?q=Test')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_results.html')
        self.assertContains(response, 'Test Blog')

    def test_delete_blog_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('delete_blog', args=[self.blog_post.slug]))
        self.assertEqual(response.status_code, 302)  # Assuming the delete_blog view redirects after deleting a blog post

        # Check if the blog post is deleted
        with self.assertRaises(Blog.DoesNotExist):
            Blog.objects.get(slug=self.blog_post.slug)