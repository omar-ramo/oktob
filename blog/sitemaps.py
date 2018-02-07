from django.contrib.sitemaps import Sitemap

from .models import Post, Tag

class PostSitemap(Sitemap):
	changefreq = 'monthly'
	priority = 0.9
	
	def items(slef):
		return Post.published.all()
		
	def lastmod(self, obj):
		return obj.updated

class TagSitemap(Sitemap):
	changefreq = 'yearly'
	priority = 0.7
	
	def items(slef):
		return Tag.objects.all()
		
	def lastmod(self, obj):
		return obj.timestamp