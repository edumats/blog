from django.urls import path, include

from .views import index, PostDetailView, PostListView, SearchView

urlpatterns = [
    path('', index, name='index'),
    path('blog/', PostListView.as_view(), name='blog'),
    path('post/<slug:slug>', PostDetailView.as_view(), name='post'),
    path('search/', SearchView.as_view(), name='search'),
]
