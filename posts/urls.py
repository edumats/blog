from django.urls import path, include

from .views import index, PostDetailView, PostListView, PostDetailView, SearchView, PostDeleteView, PostUpdateView, PostCreateView, CategoryListView

urlpatterns = [
    path('', index, name='index'),
    path('blog/', PostListView.as_view(), name='blog'),
    path('post/<slug:slug>', PostDetailView.as_view(), name='post'),
    path('post/<slug:slug>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<slug:slug>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('post/create/', PostCreateView.as_view(), name='post-create'),
    path('search/', SearchView.as_view(), name='search'),
    path('category/<str:category>', CategoryListView.as_view(), name='category_list'),
]
