from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from random import choice

def get_random_string(
			length=2, 
			allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-'
			):
	"""
	Returns a generated random string.
	The default length of 2 with the a-z, A-Z, 0-9 character set.
	"""
	return ''.join(choice(allowed_chars) for i in range(length))

def paginate_qs(qs, by=6, page=1):
	"""
	Returns requisted page queryset.
	The default objects per page is 6.
	The default page is 1.
	"""
	paginator = Paginator(qs, 6)
	try:
		paginated_qs = paginator.page(page)
	except PageNotAnInteger:
		paginated_qs = paginator.page(1)
	except EmptyPage:
		paginated_qs = paginator.page(paginator.num_pages)
	return paginated_qs