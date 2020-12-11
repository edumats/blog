from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Q
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

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
    # Receiving UnorderedObjectListWarning before overriding the queryset
    queryset = Post.objects.order_by('-timestamp')
    template_name = '../templates/blog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = Post.objects.order_by('-timestamp')[:3]
        context['category_count'] = get_category_count()
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = '../templates/post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = Post.objects.order_by('-timestamp')[:3]
        context['category_count'] = get_category_count()
        return context

class SearchView(ListView):
    paginate_by = 10
    model = Post
    template_name = '../templates/search_results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = Post.objects.order_by('-timestamp')[:3]
        context['category_count'] = get_category_count()
        return context

    def get_queryset(self):
        query = self.request.GET.get('search')
        return Post.objects.filter(
            Q(title__icontains=query) | Q(overview__icontains=query) | Q(categories__title__icontains=query)
        ).distinct()
