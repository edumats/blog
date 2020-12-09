from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.shortcuts import render
from django.views.generic.list import ListView

from .models import Post

def get_category_count():
    queryset = Post.objects.values('categories__title').annotate(Count('categories__title'))
    return queryset

def index(request):
    posts = Post.objects.filter(featured=True)
    latest_posts = Post.objects.order_by('-timestamp')[:3]
    return render(request, 'index.html', {'posts': posts, 'latest_posts': latest_posts})

class PostListView(ListView):
    paginate_by = 4
    model = Post
    template_name = '../templates/blog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = Post.objects.order_by('-timestamp')[:3]
        context['category_count'] = get_category_count()
        print(context['category_count'])
        return context

def post(request, slug):
    return render(request, 'post.html')
