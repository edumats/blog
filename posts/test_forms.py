from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User

from .forms import CreatePostForm
from .models import Author, Image

class TestForms(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='Test User', email='testuser@test.com', password='testuser123')
        self.author = Author()
        self.author.user = self.user
        self.author.profile_picture = 'profile_images/image_profile.jpg'
        self.author.save()

        self.image = Image()
        self.image.image = '/post_images/Eggplant_Parm.jpg'
        self.image.alt_tag = 'test image'
        self.image.save()

    def test_create_post_valid_data(self):
        form = CreatePostForm(data={
            'title': 'Post 1',
            'description': 'Testing a form',
            'content': '<h1>This is a test</h1> <p>Testing 1, 2, 3</p>',
            'thumbnail': self.image,
        })
        print(form.errors)
        self.assertTrue(form.is_valid())
    
    def test_create_post_no_data(self):
        form = CreatePostForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)