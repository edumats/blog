from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User

from .models import Profile

class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profile_detail.html'
    
    def get_object(self):
        current_user = User.objects.get(pk=1)
        return Profile.objects.get(user=current_user)
