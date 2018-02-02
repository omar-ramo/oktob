from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^page/(?P<page>[0-9]+)/$', views.post_list, name='post_page_list'),
    url(r'^@(?P<username>[a-zA-Z0-9_-]+)/$', views.post_user_list, name='post_user_list'),
    url(r'^tag/(?P<tag_slug>[a-zA-Z0-9_-]+)/$', views.post_tag_list, name='post_tag_list'),
    url(r'^create/$', views.post_create, name='post_create'),
    url(r'^edit/(?P<post_slug>[a-zA-Z0-9_-]+)/$', views.post_edit, name='post_edit'),
    url(r'^(?P<post_slug>[a-zA-Z0-9_-]+)/$', views.post_detail, name='post_detail'),
]