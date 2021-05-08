from django.shortcuts import render
from forum.models import Post, Category
from django.views.generic import ListView, DetailView


def category_post(request, slug):
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    context = {
        'post_list': post_list,
        'categories': Category.objects.all(),
        'num_noncategory_posts': Post.objects.filter(category=None).count(),
        'category': category
    }

    return render(
        request,
        'forum/post_list.html',
        context,
    )


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
