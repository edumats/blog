from base64 import b64decode

from django.test import TestCase
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from io import BytesIO
from PIL import Image as PIL_IMAGE
from django.core.files.base import File

from .models import Author, Category, Image, Post 

class PostTestCase(TestCase):
    @staticmethod
    def get_image_file(name='test_image.png', ext='png', size=(50, 50), color=(256, 0, 0)):
        file_obj = BytesIO()
        image = PIL_IMAGE.new("RGBA", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

    def setUp(self):
        # Need to create other models to create a complete Post object
        self.user = User.objects.create(username='Test User', email='testuser@test.com', password='testuser123')
        self.author = Author()
        self.author.user = self.user
        self.author.profile_picture = 'profile_images/image_profile.jpg'
        self.author.save()

        self.image = Image()
        self.image.image = '/post_images/Eggplant_Parm.jpg'
        self.image.alt_tag = 'test image'
        self.image.save()

        self.category1 = Category.objects.create(title='Test Category 1')
        self.category2 = Category.objects.create(title='Test Category 2')
        self.category3 = Category.objects.create(title='Test Category 3')

        # Creates the Post object
        self.post1 = Post.objects.create(
            title='Test 1 2 3', 
            description='Testing a post', 
            content='<h1>This is a test</h1> <p>Testing 1, 2, 3</p>',
            author = self.author,
            thumbnail = self.image,
            featured = True
        )
        self.post1.categories.add(self.category1, self.category2, self.category3)
    
    def test_author_methods(self):
        self.assertEqual(str(self.author), 'Test User')

    def test_category_methods(self):
        self.assertEqual(str(self.category1), 'Test Category 1')
        self.assertEqual(self.category1.get_absolute_url(), '/category/test-category-1')

    def test_image_methods(self):
        self.assertEqual(str(self.image), '/post_images/Eggplant_Parm.jpg')

    def test_post_methods(self):
        self.assertEqual(str(self.post1), 'Test 1 2 3')
        self.assertEqual(self.post1.get_absolute_url(), '/post/test-1-2-3')
        self.assertEqual(self.post1.get_update_url(), '/post/test-1-2-3/update')
        # Checks if default author is working
        self.assertEqual(self.post1.author, self.author)
