from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from blog.sitemaps import PostSitemap



sitemaps = {
    'posts':PostSitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace = 'blog')),
    path('blog/', include('django.contrib.auth.urls')),
                          
    path('sitemap.xml', sitemap, {'sitemaps':sitemaps}, name = 'django.contrib.sitemaps.views.sitemap'),
    
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
