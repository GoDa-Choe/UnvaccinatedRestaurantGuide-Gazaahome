from django.shortcuts import render
from forum.models import Post, Category
from django.views.generic import ListView, DetailView


class PostList(ListView):
    model = Post
    template_name = 'forum/post_list.html'
    ordering = '-pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['num_noncategory_posts'] = Post.objects.filter(category=None).count()

        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'forum/post_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['num_noncategory_posts'] = Post.objects.filter(category=None).count()

        return context
