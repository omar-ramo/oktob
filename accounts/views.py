from django.db.models import Count
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.generic import CreateView

from .forms import UserCreationForm

from blog.models import Post, Tag, Comment

class UserRegistrationView(CreateView):
	form_class = UserCreationForm
	template_name = 'accounts/register.html'

	def get_success_url(self):
		return reverse('accounts:login')

def profile(request):
	qs = Post.objects.filter(owner=request.user)
	paginator = Paginator(qs, 6)
	page = request.GET.get('page', 1)
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)

	hotest_tags = Tag.objects.all().annotate(posts_count=Count('posts')).order_by('posts_count')[:5]
	return render(request, 'accounts/profile.html', {'posts': posts, 'hotest_tags': hotest_tags,})