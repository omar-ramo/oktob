from django import forms

from .models import Post, Tag, Comment


class PostForm(forms.ModelForm):
	class Meta:
		model= Post
		fields = ('title', 'image', 'body', 'status', 'tags')


class CommentForm(forms.ModelForm):
	class Meta:
		model= Comment
		fields = ('body', )
		widgets = {
			'body':forms.Textarea(),
		}