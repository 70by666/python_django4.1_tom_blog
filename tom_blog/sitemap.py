from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.blog.models import Posts


class PostsSiteMap(Sitemap):
    """
    Карта сайта для статей
    """
    changefreq = 'monthly'
    priority = 0.9
    protocol = 'https'
    
    def items(self):
        return Posts.objects.all()
    
    def lastmod(self, obj):
        return obj.updated
    

class StaticSitemap(Sitemap):
    """
    Карта сайта для статичных страниц
    """
    def items(self):
        return ['index', 'contact']
    
    def location(self, item):
        return reverse(item)
