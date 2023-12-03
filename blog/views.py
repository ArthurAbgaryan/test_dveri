from django.shortcuts import render
from .models import Post

def main_list(request):
    post = Post.objects.all()
    return render(request, 'blog/post_main.html', {'post':post})
# Create your views here.
