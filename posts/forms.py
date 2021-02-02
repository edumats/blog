from django import forms
from django.forms.models import inlineformset_factory

from .models import Post, Image, Category
from .form_select_override import SelectWithPop, MultipleSelectWithPop

class UploadImage(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image', 'alt_tag']

class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title']

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'content', 'thumbnail', 'categories', 'featured']
        widgets = {
            'thumbnail': SelectWithPop(),
            'categories': MultipleSelectWithPop()
        }
