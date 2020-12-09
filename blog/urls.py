from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from posts.views import index, post, PostListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('blog/', PostListView.as_view(), name='blog'),
    path('post/<slug:slug>', post, name='post'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
