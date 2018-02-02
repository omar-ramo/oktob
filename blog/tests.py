from django.test import TestCase, Client
from django.urls import reverse, resolve

from . import views
from .models import Post, Comment, Tag

from accounts.models import User

class MySetup(TestCase):
	def setUp(self):
		user1 = User.objects.create_user('user1@user1.org', 'user1', 'password123')
		user2 = User.objects.create_user('user2@user2.org', 'user2', 'password123')
		# tag1 = Tag.objects.create(title='first tag', slug='first-tag')
		# tag1 = Tag.objects.create(title='first tag', slug='first-tag')
		#Posts of the first user
		Post.objects.create(title='first post',
							slug='first-post',
							body='first post content.',
							status='p',
							owner=user1,
			)
		Post.objects.create(title='second post',
							slug='second-post',
							body='second post content.',
							status='d',
							owner=user1,
			)
		#Posts of the second user
		Post.objects.create(title='third post',
							slug='third-post',
							body='third post content.',
							status='p',
							owner=user2,
			)
		Post.objects.create(title='fourht post',
							slug='fourht-post',
							body='fourht post content.',
							status='d',
							owner=user2,
			)
		self.client = Client()

class PostListViewTestes(MySetup):
	def setUp(self):
		super()
		self.response = self.client.get(reverse('blog:post_list'))

	def test_post_user_list_status_code(self):
		self.assertEquals(self.response.status_code, 200)

	def test_post_list_resolves(self):
		response = resolve(reverse('blog:post_list'))
		self.assertEquals(response.func.__name__, views.post_list.__name__)

	def test_post_list_contains_published_post(self):
		self.assertContains(self.response, 'first post')

	def test_post_list_not_contains_draft_post(self):
		self.assertNotContains(self.response, 'second-post')

	def test_post_list_contains_login_link(self):
		login_link = reverse('accounts:login')
		self.assertContains(self.response, login_link)

	def test_post_list_contains_register_link(self):
		register_link = reverse('accounts:register')
		self.assertContains(self.response, register_link)


class PostUserListViewTestes(MySetup):
	def setUp(self):
		super()
		self.response = self.client.get(reverse('blog:post_user_list', args=['user1']))

	def test_post_user_list_status_code(self):
		self.assertEquals(self.response.status_code, 200)
		
	def test_post_user_list_resolves(self):
		response = resolve(reverse('blog:post_user_list', args=['user1']))
		self.assertEquals(response.func.__name__, views.post_user_list.__name__)

	def test_post_user_list_contains_user_published_post(self):
		self.assertContains(self.response, 'first-post')

	def test_post_user_list_not_contains_user_draft_post(self):
		self.assertNotContains(self.response, 'second-post')

	def test_post_user_list_contains_user_published_post(self):
		self.assertContains(self.response, 'first-post')

	def test_post_user_list_not_contains_user_draft_post(self):
		self.assertNotContains(self.response, 'second-post')

	def test_post_user_list_contains_login_link(self):
		login_link = reverse('accounts:login')
		self.assertContains(self.response, login_link)

	def test_post_user_list_contains_register_link(self):
		register_link = reverse('accounts:register')
		self.assertContains(self.response, register_link)
