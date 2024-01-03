from django import template
from ..models import Post
import markdown #скаченн библиотека синтаксиса текста
from django.utils.safestring import mark_safe #фу-ия помечает результат работы как HTML-код

register = template.Library()

@register.simple_tag(name='my_tag')
def total_posts():
    return Post.objects.count()

@register.inclusion_tag('blog/later_posts.html') #тег возвр-ий готовый шаблон
def new_posts():
    new = Post.objects.order_by('-date_created')[:3]
    return {'new':new}

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
