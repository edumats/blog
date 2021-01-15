from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User

from .models import Author, Category, Image, Post 

class PostTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='Test User', email='testuser@test.com', password='testuser123')
        test_author = Author.objects.create(
            user=self.user,
            profile_picture= SimpleUploadedFile('test_image_profile.jpg', content=open('static/img/avatar-1.jpg', 'rb').read(), content_type='image/jpeg')
        )

        test_image = Image.objects.create(
            image = SimpleUploadedFile('test_image.jpg', content=open('static/img/avatar-1.jpg', 'rb').read(), content_type='image/jpeg'),
            alt_tag = 'test image'
        )

        test_category1 = Category.objects.create(title='Test Category 1')
        test_category2 = Category.objects.create(title='Test Category 2')
        test_category3 = Category.objects.create(title='Test Category 3')

        test_post1 = Post.objects.create(
            title='Test1', 
            slug='test1', 
            description='Testing a post', 
            content='<h1>This is a test</h1> <p>Testing 1, 2, 3</p>',
            author = test_author,
            thumbnail = test_image,
            featured = True
        )
        test_post1.categories.add(test_category1, test_category2, test_category3)
    
    def test_post_methods(self):
        post1 = Post.objects.get(title='Test1')
        self.assertEqual(post1.__str__(), 'Test1')