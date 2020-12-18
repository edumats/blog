from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy
from django.db.models import Count, Q
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, Category
from .forms import PostForm

def get_category_count():
    queryset = Post.objects.values('categories__title').annotate(Count('categories__title'))
    return queryset

def index(request):
    posts = Post.objects.filter(featured=True)[:3]
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

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = '__all__'
    template_name = '../templates/post_update_form.html'

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = '../templates/post_delete_form.html'
    success_url = reverse_lazy('author-list')

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    #fields = '__all__'
    template_name = '../templates/post_create_form.html'

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

class CategoryListView(ListView):
    paginate_by = 10
    model = Post
    template_name = '../templates/posts_list_by_category.html'

    def get_queryset(self):
        return Post.objects.filter(categories__title=self.kwargs['category']).order_by('-timestamp')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = Post.objects.order_by('-timestamp')[:3]
        context['category_count'] = get_category_count()
        context['category'] = self.kwargs['category']
        return context