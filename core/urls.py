from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('api/v1/accounts/', include('accounts.urls')),
    path('api/v1/chats/', include('chats.urls')),
    path('admin/', admin.site.urls),
    re_path(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT})
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
