
from django.contrib.sitemaps import Sitemap
from .models import Post
class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
def items(self):
        return Post.published.all()
def lastmod(self, obj):
      return obj.updated


# this sitemap is not working - not showing the urls for the published posts