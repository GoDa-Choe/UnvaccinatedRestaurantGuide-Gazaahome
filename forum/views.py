from django.shortcuts import render
from forum.models import Post
from django.views.generic import ListView, DetailView


class PostList(ListView):
    model = Post
    template_name = 'forum/post_list.html'
    ordering = '-pk'


class PostDetail(DetailView):
    model = Post
    template_name = 'forum/post_detail.html'
