from django import forms
from .models import Post, Image, Category
from .widgets import RelatedFieldWidgetCanAdd

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'description', 'content', 'thumbnail', 'categories', 'featured']
        widgets = {
            'thumbnail': RelatedFieldWidgetCanAdd(Image),
            'categories': RelatedFieldWidgetCanAdd(Category)
        }
