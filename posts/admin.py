from django.contrib import admin
from .models import Author, Category, Post

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
