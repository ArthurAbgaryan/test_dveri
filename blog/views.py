from django.shortcuts import render,redirect,get_object_or_404
from .models import Post,Comment
from django.views.generic import DetailView, DeleteView,UpdateView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.urls import reverse_lazy
from .forms import PostForm,CommentForm
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from taggit.models import Tag #имп-ли модель тегов
from django.db.models import Count

def main_list(request, tag_slug = None):
    post = Post.objects.order_by('-date_created')
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug = tag_slug) #получ. все теги статьи
        post = Post.objects.filter(tags__in = [tag])# список всех оьектов с полученным тегом
    return render(request, 'blog/post_main.html', {'post':post, 'tag': tag})

'''
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
'''

def post_detail(request, pk, slug):
    page = Post.objects.get(id = pk, slug = slug)
    context = {}

    if request.method == 'POST':
        comments_qs = None
        new_comment = None
        comment_form = CommentForm(request.POST or None)
        signal = True
        if comment_form.is_valid():
            '''Вариань исп-ия из книги
            new_comment = comment_form.save(commit=False) #метод save создает обьект, commit = False не сохраняет обьект
            new_comment.post = page
            new_comment.save()
            '''
            #Вариант использования из уроков
            body = request.POST.get('body')
            comment = Comment.objects.create(
                post = page,
                body = body,
                name_author = request.user,
            )
            comment.save()
            signal = True

    else:
        comment_form = CommentForm()
        signal = False

    total_comment = page.comment_post.all()

    saved = False
    if page.saved_post.filter(id = request.user.id).exists():
        saved = True

    liked = False
    if page.like.filter(id = request.user.id).exists():
        liked = True



    '''Формирование списка похожих статей'''
    posts_tags = page.tags.values_list('id', flat = True)#получили спи-ок из id тегов нашей статьи
    all_posts_tag = Post.objects.filter(tags__in = posts_tags).exclude(id = page.id)#получили статьи с похожими тегами искл-ая нашу статью
    all_posts_tag = all_posts_tag.annotate(sum_tag=Count('tags')).order_by('-sum_tag','-date_created')[:4]#пол-ли 4 статьи с последними тегами и свежей даты

    context['recomend'] = all_posts_tag
    context['signal'] = signal
    context['total_comment'] = total_comment
    context['form'] = comment_form
    context['page'] = page
    context['saved'] = saved
    context['liked'] = liked
    if request.is_ajax():
        html = render_to_string('blog/comment_form.html',context, request=request)
        return JsonResponse({'form':html})
    return render(request, 'blog/post_detail.html', context)


class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('main_list')
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    template_name = 'blog/post_update.html'
    fields = ['title','body']
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    #success_url = 'blog/post_detail.html'
'''
class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','body']
    template_name = 'blog/post_form.html'


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
'''

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            t = request.POST.get('title')
            b = request.POST.get('body')
            new_form = Post.objects.create(
                title = t,
                body = b,
                author = request.user
            )

            new_form.save()
            messages.success(request, "Message sent.")

            return redirect ('main_list')

            #return HttpResponse('blog/post_main.html')

    else:
        form = PostForm()
    return render(request, 'blog/post_form.html',{'form':form})

@login_required
def save_posts(request):
    name_user = request.user
    saves = Post.objects.filter(saved_post=name_user)
    return render(request,'blog/saves_posts.html', {'saves':saves})

@login_required
def like_post_ajax(request):
    post = get_object_or_404(Post, id = request.POST.get('id'))
    liked = False
    if post.like.filter(id = request.user.id).exists():
        post.like.remove(request.user)
        liked = False
    else:
        post.like.add(request.user)
        liked = True

    context = {
        'liked': liked,
        'page':post,
    }
    if request.is_ajax():
        html = render_to_string('blog/like_ajax.html', context, request=request)
        return JsonResponse({'form':html})




@login_required
def save_posts_ajax(request):
    post = get_object_or_404(Post, id = request.POST.get('id'))
    saved = False
    if post.saved_post.filter(id = request.user.id).exists():
        post.saved_post.remove(request.user)
        saved = False
    else:
        post.saved_post.add(request.user)
        saved = True

    context = {
        'page':post,
        'saved': saved,
        'total_save': post.save_count(),
    }
    if request.is_ajax():
        html = render_to_string('blog/save_post_ajax.html', context, request=request)
        return JsonResponse ({'form':html})
