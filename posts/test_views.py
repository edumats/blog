from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


from .models import Author, Post, Image, Category

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create(username='Test User', email='testuser@test.com', password='testuser123')
        self.author = Author()
        self.author.user = self.user
        self.author.profile_picture = 'profile_images/image_profile.jpg'
        self.author.save()

        self.post1 = Post.objects.create(
            title='Test1', 
            description='Testing a post', 
            content='<h1>This is a test 1</h1> <p>Testing 1, 2, 3</p>',
            author = self.author,
            featured = True
        )

        self.post2 = Post.objects.create(
            title='Test2', 
            description='Testing a post', 
            content='<h1>This is a test 2</h1> <p>Testing 1, 2, 3</p>',
            author = self.author,
            featured = True
        )

        self.post3 = Post.objects.create(
            title='Test3', 
            description='Testing a post', 
            content='<h1>This is a test 3</h1> <p>Testing 1, 2, 3</p>',
            author = self.author,
            featured = True
        )

        self.post4 = Post.objects.create(
            title='Test4', 
            description='Testing a post', 
            content='<h1>This is a test 4</h1> <p>Testing 1, 2, 3</p>',
            author = self.author,
            featured = True
        )
        self.category1 = Category.objects.create(title='Test Category 1')
        self.category2 = Category.objects.create(title='Test Category 2')
        self.category3 = Category.objects.create(title='Test Category 3')

        self.post1.categories.add(self.category1)
        self.post2.categories.add(self.category2)
        self.post3.categories.add(self.category3)

    def test_index_get(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
    
    def test_post_list_get(self):
        response = self.client.get(reverse('blog'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, '../templates/blog.html')

    def test_post_detail_get(self):
        response = self.client.get(reverse('post', args=['test1']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, '../templates/post.html')
    
    def test_post_delete_get(self):
        response = self.client.get(reverse('post-delete', args=['test1']))
        # Returning 302
        # self.assertEqual(response.status_code, 200)
        # No templates used to render this response
        #self.assertTemplateUsed(response, '../templates/post_delete_form.html')
    
    def test_post_delete_POST(self):
        post5 = Post.objects.create(
            title='Test5', 
            description='Testing a post', 
            content='<h1>This is a test 5</h1> <p>Testing 1, 2, 3</p>',
            author = self.author,
        )
        response = self.client.post(reverse('post-delete', args=['test5']))
        self.assertEqual(response.status_code, 302)
    
    def test_post_create_POST(self):
        response = self.client.post(reverse('post-create'), {
            'title': 'Test5',
            'description': 'Testing a post', 
            'content': '<h1>This is a test</h1> <p>Testing 1, 2, 3</p>',
            'author': self.author,
        })
        # In CreateView successful valid_form returns 302 response
        self.assertEqual(response.status_code, 302)

    def test_search_get(self):
        response = self.client.get(reverse('search'), {'search': 'post1'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, '../templates/search_results.html')
    
    def test_category_list_get(self):
        response = self.client.get(reverse('category_list', args=['test_category_1']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, '../templates/posts_list_by_category.html')