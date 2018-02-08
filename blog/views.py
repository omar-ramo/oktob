from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from .forms import PostForm, CommentForm
from .models import Post, Tag, Comment
from .utils import paginate_qs

def post_list(request, page=1):
	qs = Post.published.all()
	posts = paginate_qs(qs=qs, by=6, page=page)

	hotest_tags = Tag.objects.all().annotate(posts_count=Count('posts')).order_by('-posts_count')[:5]
	return render(request, 'blog/post_list.html', {'posts': posts, 'hotest_tags': hotest_tags,})

def post_user_list(request, username, page=1):
	qs = Post.published.filter(owner__username__exact=username)
	posts = paginate_qs(qs=qs, by=6, page=page)

	hotest_tags = Tag.objects.all().annotate(posts_count=Count('posts')).order_by('-posts_count')[:5]
	return render(request, 'blog/post_user_list.html', {'posts': posts, 'username': username, 'hotest_tags': hotest_tags,})

def post_tag_list(request, tag_slug, page=1):
	tag = get_object_or_404(Tag, slug__exact=tag_slug)
	qs = tag.posts.filter(status='p')
	posts = paginate_qs(qs=qs, by=6, page=page)

	hotest_tags = Tag.objects.all().annotate(posts_count=Count('posts')).order_by('-posts_count')[:5]
	return render(request, 'blog/post_tag_list.html', {'tag': tag, 'posts': posts, 'hotest_tags': hotest_tags,})

@login_required
def post_create(request):
	if request.method == 'GET':
		form = PostForm()
		return render(request, 'blog/post_create.html', {'form': form})
	elif request.method == 'POST':
		form = PostForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			new_post = form.save(commit=False)
			new_post.owner = request.user
			new_post.save()
			messages.add_message(request, messages.SUCCESS, 'The post was created successfly.')
			return redirect(new_post)
		messages.add_message(request, messages.WARNING, 'Please correct the errors in the form.')
		return render(request, 'blog/post_create.html', {'form': form})

@login_required
def post_edit(request, post_slug):
	post = get_object_or_404(Post.published,owner=request.user, slug__exact=post_slug)
	if request.method == 'GET':
		form = PostForm(instance=post)
		return render(request, 'blog/post_edit.html', {'form': form})
	elif request.method == 'POST':
		form = PostForm(request.POST or None, request.FILES or None, instance=post)
		if post.owner == request.user:
			if form.is_valid():
				form.save()
				messages.add_message(request, messages.SUCCESS, 'The post was updated successfly.')
				return redirect(post)
			messages.add_message(request, messages.WARNING, 'Please correct the errors in the form.')
			return render(request, 'blog/post_edit.html', {'form': form})
		else:
			raise HttpResponseForbidden()


def post_detail(request, post_slug):
	if request.method == 'GET':
		comment_form = CommentForm()
		if request.user.is_authenticated:
			#if you are the owner of a draft post, you will be able to see it. otherwise 404
			qs = Post.objects.filter(slug__exact=post_slug).filter(Q(status='d') & Q(owner=request.user) | Q(status='p'))
		else:
			qs = Post.published.filter(slug__exact=post_slug)
		if not qs.exists():
			raise Http404()
		post = qs.first()
		post.views_count= post.views_count + 1
		post.save()
		hotest_tags = Tag.objects.all().annotate(posts_count=Count('posts')).order_by('-posts_count')[:5]
		return render(request, 'blog/post_detail.html', {'post': post, 'hotest_tags': hotest_tags, 'comment_form': comment_form})

	elif request.method=='POST':
		comment_form = CommentForm(request.POST)
		post = get_object_or_404(Post.published, slug__exact=post_slug)
		if request.user.is_authenticated:
			if comment_form.is_valid():
				new_comment = comment_form.save(commit=False)
				new_comment.owner = request.user
				new_comment.post = post
				new_comment.save()
				messages.add_message(request, messages.SUCCESS, 'You comment was added successfly.')
				return redirect(post)
			else:
				hotest_tags = Tag.objects.all().annotate(posts_count=Count('posts')).order_by('-posts_count')[:5]
				messages.add_message(request, messages.WARNING, 'Please correct the errors in the form.')
				return render(request, 'blog/post_detail.html', {'post': post, 'hotest_tags': hotest_tags, 'comment_form': comment_form})
		else:
			messages.add_message(request, messages.WARNING, 'You must be logged in to comment.')
			return redirect('{}?next={}'.format(settings.LOGIN_URL, post.get_absolute_url()))
