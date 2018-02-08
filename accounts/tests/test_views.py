from django.conf import settings
from django.test import TestCase, Client
from django.urls import reverse, resolve

from .. import views
from ..forms import UserCreationForm
from ..models import User

from accounts.models import User

		
class SignupViewTests(TestCase):
	@classmethod
	def setUpTestData(self):
		self.signup_url = reverse('accounts:register')
		self.login_url = reverse('accounts:login')

	def test_signup_view_status_code(self):
		response = self.client.get(self.signup_url)
		self.assertEquals(response.status_code, 200)

	def test_post_list_resolves(self):
		response = resolve(self.signup_url)
		self.assertEquals(response.func.__name__, views.SignupView.as_view().__name__)

	def test_csrf(self):
		response = self.client.get(self.signup_url)
		self.assertContains(response, 'csrfmiddlewaretoken')


	def test_signup_view_contains_form(self):
		response = self.client.get(self.signup_url)
		self.assertContains(response, '<form ')
		self.assertIsInstance(response.context.get('form'),UserCreationForm)


	def test_signup_view_with_valid_data(self):
		data = {
			'email': 'jack@jack.org',
			'username': 'jack',
			'password1': 'password123',
			'password2': 'password123',
		}
		response = self.client.post(self.signup_url, data=data)
		self.assertRedirects(response, self.login_url)
		self.assertTrue(User.objects.exists())


	def test_signup_view_with_empty_data(self):
		data = {
			'email': '',
			'username': '',
			'password1': '',
			'password2': '',
		}
		response = self.client.post(self.signup_url, data=data)
		self.assertEquals(response.status_code, 200)
		self.assertTrue(response.context.get('form').errors)
		self.assertFalse(User.objects.exists())

	def test_signup_view_with_invalid_email(self):
		data = {
			'email': 'jackjack.org',
			'username': 'jack',
			'password1': 'password123',
			'password2': 'password123',
		}
		response = self.client.post(self.signup_url, data=data)
		self.assertEquals(response.status_code, 200)
		self.assertTrue(response.context.get('form').errors)
		self.assertFalse(User.objects.exists())

	def test_signup_view_with_invalid_username(self):
		data = {
			'email': 'jack@jack.org',
			'username': 'ja@$ck',
			'password1': 'password123',
			'password2': 'password123',
		}
		response = self.client.post(self.signup_url, data=data)
		self.assertEquals(response.status_code, 200)
		self.assertTrue(response.context.get('form').errors)
		self.assertFalse(User.objects.exists())

	def test_signup_view_with_invalid_dismatch_password(self):
		data = {
			'email': 'jack@jack.org',
			'username': 'jack',
			'password1': 'password123',
			'password2': 'password',
		}
		response = self.client.post(self.signup_url, data=data)
		self.assertEquals(response.status_code, 200)
		self.assertTrue(response.context.get('form').errors)
		self.assertFalse(User.objects.exists())


	def test_signup_view_with_already_used_email(self):
		data1 = {
			'email': 'jack@jack.org',
			'username': 'jack',
			'password1': 'password123',
			'password2': 'password123',
		}
		data2 = {
			'email': 'jack@jack.org',
			'username': 'jackie',
			'password1': 'mysecret',
			'password2': 'mysecret',
		}
		#Creating the first user
		self.client.post(self.signup_url, data=data1)
		#The second user
		response = self.client.post(self.signup_url, data=data2)
		self.assertEquals(response.status_code, 200)
		self.assertTrue(response.context.get('form').errors)
		self.assertEquals(User.objects.count(), 1)


	def test_signup_view_with_already_used_username(self):
		data1 = {
			'email': 'jack@jack.org',
			'username': 'jack',
			'password1': 'password123',
			'password2': 'password123',
		}
		data2 = {
			'email': 'tom@tom.org',
			'username': 'jack',
			'password1': 'password123',
			'password2': 'password123',
		}
		#Creating the first user
		self.client.post(self.signup_url, data=data1)
		#The second user
		response = self.client.post(self.signup_url, data=data2)
		self.assertEquals(response.status_code, 200)
		self.assertTrue(response.context.get('form').errors)
		self.assertEquals(User.objects.count(), 1)
