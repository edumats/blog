from django import forms
from django.forms.models import inlineformset_factory

from .models import Post, Image, Category
from .widgets import RelatedFieldWidgetCanAdd

class UploadImage(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image', 'alt_tag']

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'description', 'content', 'thumbnail', 'categories', 'featured']
        widgets = {
            'thumbnail': RelatedFieldWidgetCanAdd(Image),
            'categories': RelatedFieldWidgetCanAdd(Category)
        }

