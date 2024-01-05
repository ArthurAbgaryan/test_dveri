from .models import Post,Comment
from django.forms import ModelForm
from django import forms
class Search(forms.Form):
    search = forms.CharField(max_length=100)


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title','body','tags']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
