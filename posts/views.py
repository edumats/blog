from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy, reverse
from django.db.models import Count, Q
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify
from django.http import HttpResponseRedirect

from .models import Author, Post, Category, Image
from .forms import CreatePostForm, CreateCategoryForm

def get_category_count():
    queryset = Post.objects.values('categories__title').annotate(Count('categories__title'))
    return queryset

def latest_posts():
    queryset = Post.objects.order_by('-timestamp')[:3]
    return queryset

class IndexView(ListView):
    model = Post
    queryset = Post.objects.filter(featured=True)[:3]
    template_name = 'index.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_posts'] = latest_posts()
        return context

class PostListView(ListView):
    paginate_by = 4
    model = Post
    # Receiving UnorderedObjectListWarning before overriding the queryset
    queryset = Post.objects.order_by('-timestamp')
    template_name = '../templates/blog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = latest_posts()
        context['category_count'] = get_category_count()
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = '../templates/post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = latest_posts()
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
    form_class = CreatePostForm
    template_name = '../templates/post_create_form.html'

    def form_valid(self, form):
        current_user = Author.objects.get(user=self.request.user)
        form.instance.author = current_user
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_category'] = CreateCategoryForm
        return context


class SearchView(ListView):
    paginate_by = 10
    model = Post
    template_name = '../templates/search_results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = latest_posts()
        context['category_count'] = get_category_count()
        return context

    def get_queryset(self):
        query = self.request.GET.get('search')
        return Post.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(categories__title__icontains=query)
        ).distinct().order_by('-timestamp')

class CategoryListView(ListView):
    paginate_by = 10
    model = Post
    template_name = '../templates/posts_list_by_category.html'

    def get_queryset(self):
        return Post.objects.filter(categories__title=self.kwargs['category']).order_by('-timestamp')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = latest_posts()
        context['category_count'] = get_category_count()
        context['category'] = self.kwargs['category']
        return context

def CreateCategoryView(request):
    print('hi')
    if request.method == 'POST':
        print('posted')
        form = CreateCategoryForm(request.POST)
        if form.is_valid():
            print('form is valid')
            form.save()
            return HttpResponseRedirect(reverse('post-create'))