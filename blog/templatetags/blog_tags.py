from django import template
from ..models import Post

register = template.Library()

@register.simple_tag(name='my_tag')
def total_posts():
    return Post.objects.count()

@register.inclusion_tag('blog/later_posts.html')
def new_posts():
    new = Post.objects.order_by('-date_created')[:3]
    return {'new':new}

