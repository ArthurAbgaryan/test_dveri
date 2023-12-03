from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name = 'Название')
    body = models.TextField(max_length=1000, blank=True, null = True)
    slug = models.SlugField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    like = models.ManyToManyField(User, related_name = 'like_post')
    save = models.ManyToManyField(User,related_name= 'save_post')
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name= 'post_author')

    def like_count(self):
        return self.like.count()
    def save_count(self):
        return self.save.count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse ('post_detail',kwargs= {'pk':self.pk, 'slug':self.slug})
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
# Create your models here.
