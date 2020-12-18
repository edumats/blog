from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from tinymce.models import HTMLField

User = get_user_model()

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    def __str__(self):
        return self.user.username

class Category(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_list', kwargs={
            'category': self.title
        })

class Post(models.Model):
    # This title is used for page title and is limited to 60 chracters for better SEO
    title = models.CharField(max_length=60, help_text='Try placing important keywords first')
    slug = models.SlugField()
    overview = models.TextField()
    content = HTMLField()
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField()
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/post/{self.slug}'

    def get_update_url(self):
        return reverse('post-update', kwargs={
            'slug': self.slug
        })

    def get_delete_url(self):
        return reverse('post-delete', kwargs={
            'slug': self.slug
        })
