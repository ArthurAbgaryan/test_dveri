from django.contrib import admin
from .models import Post, Comment
# Register your models here.

@admin.register(Post)
class AdminPost(admin.ModelAdmin):
    list_display = ['title','date_created','author']
    prepopulated_fields = {'slug':('title',)}

@admin.register(Comment)
class AdminComment(admin.ModelAdmin):
    list_display = ['post','name_author','date_created']