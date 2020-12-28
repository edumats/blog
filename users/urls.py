from django.urls import path

from .views import ProfileDetailView

urlpatterns = [
    path('<str:user>/', ProfileDetailView.as_view(), name='profile-detail'),
]