from django.contrib.syndication.views import Feed
from .models import Post
from django.urls import reverse
from django.template.defaultfilters import truncatewords

class PostFeed(Feed):

    title = 'My blog'
    link = '/blog/'
    description = 'New post of my blog'

    def items(self):
        return Post.objects.all()[:5]

    def items_title(self, item):
        return item.title

    def items_description(self, item):
        return truncatewords(item.body, 30)