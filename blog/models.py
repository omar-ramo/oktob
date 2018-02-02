from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from .utils import get_random_string

from accounts.models import User

class PostManager(models.Manager):
	def get_queryset(self, *args, **kwargs):
		qs = super(PostManager, self).get_queryset(*args, **kwargs)
		return qs.filter(status='p')

class Tag(models.Model):
	title = models.CharField(max_length=31)
	slug = models.SlugField(max_length=33, unique=True, blank=True)
	owner = models.ForeignKey(User, related_name='tags', on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)

	def save(self, *args, **kwargs):
		if(not self.id):
			slug = slugify(self.title)
			qs = Tag.objects.filter(slug__iexact=slug)
			while(qs.exists() and len(slug) <33):
				slug += get_random_string()
				qs = Tag.objects.filter(slug__iexact=slug)
			self.slug = slug
		super(Tag, self).save(*args, **kwargs)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('blog:post_tag_list', kwargs={'tag_slug': self.slug})


class Post(models.Model):
	STATUS_CHOICES = (
		('d', 'Draft'),
        ('p', 'Public'),
	)
	title = models.CharField(max_length=127)
	slug = models.SlugField(max_length=129, unique=True, blank=True)
	body = models.TextField()
	image = models.ImageField(upload_to='posts/%Y/%m/', null=True, blank=True)
	status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='p')
	views_count = models.IntegerField(default=0)
	owner = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
	tags = models.ManyToManyField(Tag, related_name='posts', blank=True, help_text='Press ctrl to select multiple tags.')
	timestamp = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	published = PostManager()
	objects = models.Manager()

	class Meta:
		ordering = ('-timestamp', )

	def save(self, *args, **kwargs):
		if(not self.id):
			slug = slugify(self.title)
			if slug in ['page', 'create', 'edit']:
				slug += get_random_string()
			qs = Post.objects.filter(slug__iexact=slug)
			while(qs.exists() and len(slug) <129):
				slug += get_random_string()
				qs = Post.objects.filter(slug__iexact=slug)
			self.slug = slug
		super(Post, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('blog:post_detail', kwargs={'post_slug': self.slug})

	def get_edit_url(self):
		return reverse('blog:post_edit', kwargs={'post_slug': self.slug})

	def get_description(self):
		return self.body[:150]

	def get_comments_count(self):
		return self.comments.count()




	def __str__(self):
		return self.title



class Comment(models.Model):
	body = models.CharField(max_length=511)
	owner = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
	post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)

	def __str__(self):
		return 'By: {}, On: {}'.format(self.owner, self.post)