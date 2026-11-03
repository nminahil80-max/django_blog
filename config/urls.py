from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from blogs import views as blog_views
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('contact/', include('contact.urls')),
    # Homepage
    path('', blog_views.blog_list, name='home'),

    path('accounts/', include('accounts.urls')),
    path('blogs/', include('blogs.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('interactions/', include('interactions.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
    