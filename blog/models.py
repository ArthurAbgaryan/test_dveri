from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import pre_save
from pytils.translit import slugify
from django.dispatch import receiver
from taggit.managers import TaggableManager #модель тэггов , ранее мы установиили через pip django_taggit
class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name = 'Название')
    body = models.TextField(max_length=1000, blank=True, null = True)
    slug = models.SlugField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    saved_post = models.ManyToManyField(User, related_name= 'save_post',blank = True)
    like = models.ManyToManyField(User,related_name='like_post', blank=True)
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name= 'post_author')
    tags = TaggableManager()


    def like_count(self):
        return self.like.count()
    def save_count(self):
        return self.saved_post.count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse ('post_detail',kwargs= {'pk':self.pk, 'slug':self.slug})
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

@receiver(pre_save, sender = Post)
def prepopulated_slug(sender,instance,**kwargs):
    instance.slug = slugify(instance.title)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name = 'comment_post')
    body = models.TextField( max_length=1000)
    name_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_comment')
    like1_comment = models.ManyToManyField(User, blank=True, related_name='like_comment')
    replay2_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True,related_name='replay_comment')
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "%s - %s - %s" %(self.post.title, self.name_author, self.id)

    def total_like_comment(self):
        return self.like_comment.count()
    def total_replay_comment(self):
        return self.replay_comment.count()

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk':self.pk})
    # Create your models here.
