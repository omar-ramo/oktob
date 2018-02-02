from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models


class UserManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		""" Creates an saves the user with the given credentials """
		if(not email):
			raise ValueError('Every user should have an email address.')

		if(not username):
			raise ValueError('Every user should have a first name.')

		user = self.model(email=self.normalize_email(email), username=username)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_staffuser(self, email, username, password=None):
		user = self.create_user(email, username, password=None)
		user.staff = True
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password=None):
		user = self.create_user(email, username, password=None)
		user.staff = True
		user.admin = True
		user.save(using=self._db)
		return user

class User(AbstractBaseUser):
	email = models.EmailField('Email address', max_length=255, unique=True)
	username = models.SlugField(max_length=31, unique=True)
	active = models.BooleanField(default=True)
	staff = models.BooleanField(default=False)
	admin = models.BooleanField(default=False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	objects = UserManager()

	def __str__(self):
		return self.email

	def get_full_name(self):
		return self.email

	def get_short_name(self):
		return self.username

	def has_perm(self, perm, obj=None):
		"Does the user have a specific permission?"
		# Simplest possible answer: Yes, always
		return True
		
	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?"
		# Simplest possible answer: Yes, always
		return True
		
	@property
	def is_staff(self):
		"Is the user a member of staff?"
		return self.staff
		
	@property
	def is_admin(self):
		"Is the user a admin member?"
		return self.admin
		
	@property
	def is_active(self):
		"Is the user active?"
		return self.active

