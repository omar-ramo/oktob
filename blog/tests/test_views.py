from django.conf import settings
from django.test import TestCase, Client
from django.urls import reverse, resolve

from .. import views
from ..forms import PostForm
from ..models import Post, Comment, Tag

from accounts.models import User

class MySetup(TestCase):
	"""
	the base setup for the views's tests.
	"""
	@classmethod
	def setUpTestData(cls):
		user1 = User.objects.create_user('user1@user1.org', 'user1', 'password123')
		user2 = User.objects.create_user('user2@user2.org', 'user2', 'password123')
		tag1 = Tag.objects.create(title='Design', slug='design', owner=user1)
		#For every user, we create 1 published post and 1 draf post.
		users = (user1, user2)
		i=0
		for user in users:
			i+=1
			p1 = Post.objects.create(title='test post %d'%i,
						slug='test-post-%d'%i,
						body='test post content.',
						status='p',
						owner=user,
			)
			p1.tags.add(tag1)
			p2 = Post.objects.create(title='test draft post %d'%i,
						slug='test-draft-post %d'%i,
						body='test draft post content.',
						status='d',
							owner=user1,
			)
			p2.tags.add(tag1)
		
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
		self.assertContains(self.response, 'test post 1')

	def test_post_list_not_contains_draft_post(self):
		self.assertNotContains(self.response, 'test draft post 1')

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
		self.assertContains(self.response, 'test post 1')

	def test_post_user_list_not_contains_user_draft_post(self):
		self.assertNotContains(self.response, 'test draft post 1')

	def test_post_user_list_not_contains_other_user_published_post(self):
		self.assertNotContains(self.response, 'test post 2')

	def test_post_user_list_not_contains_other_user_draft_post(self):
		self.assertNotContains(self.response, 'test draft post 2')

	def test_post_user_list_contains_login_link(self):
		login_link = reverse('accounts:login')
		self.assertContains(self.response, login_link)

	def test_post_user_list_contains_register_link(self):
		register_link = reverse('accounts:register')
		self.assertContains(self.response, register_link)

class PostTagListViewTestes(MySetup):
	def setUp(self):
		super()
		self.response = self.client.get(reverse('blog:post_tag_list', args=['design']))

	def test_post_tag_list_status_code(self):
		self.assertEquals(self.response.status_code, 200)
		
	def test_post_tag_list_resolves(self):
		response = resolve(reverse('blog:post_tag_list', args=['design']))
		self.assertEquals(response.func.__name__, views.post_tag_list.__name__)

	def test_post_tag_list_contains_user_published_post(self):
		self.assertContains(self.response, 'test post 1')

	def test_post_tag_list_not_contains_user_draft_post(self):
		self.assertNotContains(self.response, 'test draft post 1')

	def test_post_user_list_contains_login_link(self):
		login_link = reverse('accounts:login')
		self.assertContains(self.response, login_link)

	def test_post_user_list_contains_register_link(self):
		register_link = reverse('accounts:register')
		self.assertContains(self.response, register_link)

class PostCreateTests(TestCase):
	data = {
			'title': 'hello world!',
			'body': 'some content',
			'status': 'p',
		}
	post_create_url = reverse('blog:post_create')
	login_url = reverse(settings.LOGIN_URL)

	@classmethod
	def setUpTestData(cls):
		user1 = User.objects.create_user('user1@user1.org', 'user1', 'password123')

	def test_csrf(self):
		#Login
		self.client.post(self.login_url, data={'username': 'user1@user1.org', 'password': 'password123'})
		response = self.client.get(self.post_create_url)
		self.assertContains(response, 'csrfmiddlewaretoken')

	def test_contains_form(self):
		#Login
		self.client.post(self.login_url, data={'username': 'user1@user1.org', 'password': 'password123'})
		response = self.client.get(self.post_create_url)
		self.assertContains(response, '<form ')
		self.assertIsInstance(response.context['form'], PostForm)

	def test_non_logged_in_user_is_redirected_to_login_url(self):
		response = self.client.post(self.post_create_url, data=self.data)
		self.assertRedirects(response, '{}?next={}'.format(self.login_url, self.post_create_url))

	def test_create_post_with_valid_data(self):
		#Login
		self.client.post(self.login_url, data={'username': 'user1@user1.org', 'password': 'password123'})
		response = self.client.post(self.post_create_url, data=self.data)
		self.assertRedirects(response, reverse('blog:post_detail', args=['hello-world']))
		self.assertTrue(Post.published.exists())

	# def test_create_post_with_invalid_data(self):
	# 	#Login
	# 	self.client.post(self.login_url, data={'username': 'user1@user1.org', 'password': 'password123'})
	# 	response = self.client.post(self.post_create_url, data={})
	# 	self.assertEquals(response.status_code, 200)
	# 	self.assertTrue(response.context['form'].errors)
	# 	self.assertFalse(Post.published.exists())

	def test_create_post_with_empty_data(self):
		data = {
				'title': '',
				'body': '',
				'status': '',
			}
		#Login
		self.client.post(self.login_url, data={'username': 'user1@user1.org', 'password': 'password123'})
		response = self.client.post(self.post_create_url, data=data)
		self.assertEquals(response.status_code, 200)
		self.assertTrue(response.context['form'].errors)
		self.assertFalse(Post.published.exists())
		
class PostEditTests(TestCase):
	@classmethod
	def setUpTestData(cls):
		user1 = User.objects.create_user('user1@user1.org', 'user1', 'password123')
		user2 = User.objects.create_user('user2@user2.org', 'user2', 'password123')
		Post.objects.create(title='Current title',
						body='current post content.',
						status='p',
						owner=user1,
			)
			
	data = {
			'title': 'New title',
			'body': 'New content',
			'status': 'p',
		}
	post_edit_url = reverse('blog:post_edit', args=['current-title'])
	login_url = reverse(settings.LOGIN_URL)

	def test_csrf(self):
		#Login
		self.client.post(self.login_url, data={'username': 'user1@user1.org', 'password': 'password123'})
		response = self.client.get(self.post_edit_url)
		self.assertContains(response, 'csrfmiddlewaretoken')

	def test_contains_form(self):
		#Login
		self.client.post(self.login_url, data={'username': 'user1@user1.org', 'password': 'password123'})
		response = self.client.get(self.post_edit_url)
		self.assertContains(response, '<form ')
		self.assertIsInstance(response.context['form'], PostForm)

	def test_non_logged_in_user_is_redirected_to_login_url(self):
		response = self.client.post(self.post_edit_url, data=self.data)
		self.assertRedirects(response, '{}?next={}'.format(self.login_url, self.post_edit_url))

	def test_edit_post_with_valid_data(self):
		#Login
		self.client.post(self.login_url, data={'username': 'user1@user1.org', 'password': 'password123'})
		response = self.client.post(self.post_edit_url, data=self.data)
		self.assertRedirects(response, reverse('blog:post_detail', args=['current-title']))
		new_response = self.client.get(reverse('blog:post_detail', args=['current-title']))
		self.assertContains(new_response, 'New title')

	def test_edit_post_with_empty_data(self):
		data = {
				'title': '',
				'body': '',
				'status': '',
			}
		#Login
		self.client.post(self.login_url, data={'username': 'user1@user1.org', 'password': 'password123'})
		response = self.client.post(self.post_edit_url, data=data)
		self.assertEquals(response.status_code, 200)
		self.assertTrue(response.context['form'].errors)

	def test_edit_post_if_user_not_owner(self):
		#Login
		self.client.post(self.login_url, data={'username': 'user2@user2.org', 'password': 'password123'})
		response = self.client.post(self.post_edit_url, data=self.data)
		self.assertEquals(response.status_code, 404)
		
class PostDetailTests(TestCase):
	@classmethod
	def setUpTestData(cls):
		user1 = User.objects.create_user('user1@user1.org', 'user1', 'password123')
		user2 = User.objects.create_user('user2@user2.org', 'user2', 'password123')
		#A public post of user1
		Post.objects.create(title='first title',
						body='first post content.',
						status='p',
						owner=user1,
			)
		#A draft post of user1
		Post.objects.create(title='Second title',
						body='Second post content.',
						status='d',
						owner=user1,
			)
	first_post_url = reverse('blog:post_detail', args=['first-title'])
	first_post_edit_url = reverse('blog:post_edit', args=['first-title'])
	second_post_url = reverse('blog:post_detail', args=['second-title'])
	login_url = reverse(settings.LOGIN_URL)

	def test_status_code(self):
		response = self.client.get(self.first_post_url)
		self.assertEquals(response.status_code, 200)

	def test_non_logged_in_user_cant_see_draft(self):
		response = self.client.get(self.second_post_url)
		self.assertEquals(response.status_code, 404)

	def test_non_owner_user_cant_see_draft(self):
		#Login
		self.client.post(self.login_url, data={'username': 'user2@user2.org', 'password': 'password123'})
		response = self.client.get(self.second_post_url)
		self.assertEquals(response.status_code, 404)

	def test_non_logged_in_user_cant_see_comment_form(self):
		response = self.client.get(self.first_post_url)
		self.assertNotContains(response, '<form ')

	def test_non_logged_in_user_cant_see_edit_post_link(self):
		response = self.client.get(self.first_post_url)
		self.assertNotContains(response, self.first_post_edit_url)

	def test_non_owner_user_cant_see_edit_post_link(self):
		#Login
		self.client.post(self.login_url, data={'username': 'user2@user2.org', 'password': 'password123'})
		response = self.client.get(self.first_post_url)
		self.assertNotContains(response, self.first_post_edit_url)

	