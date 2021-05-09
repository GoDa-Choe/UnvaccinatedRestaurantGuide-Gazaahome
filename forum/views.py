from django.shortcuts import render, redirect
from forum.models import Post, Category, Tag
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'head_image', 'category', 'tags']
    template_name = 'forum/post_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super(PostUpdate, self).get_context_data()
        if self.object.tags.exists():
            tags_str_list = []
            for tag in self.object.tags.all():
                tags_str_list.append(tag.name)
            context['tags_str_default'] = '#' + '#'.join(tags_str_list)

        return context

    def form_valid(self, form):
        response = super(PostUpdate, self).form_valid(form)
        self.object.tags.clear()

        tags_str = self.request.POST.get('tags_str')

        if tags_str:
            tags_str = tags_str.strip(' #')
            tags_str = tags_str.replace(',', '#')
            tags_list = tags_str.split('#')

            for tag in tags_list:
                tag = tag.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=tag)
                if is_tag_created:
                    tag.slug = slugify(tag, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)

        return response


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'head_image', 'category']

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            response = super(PostCreate, self).form_valid(form)

            tags_str = self.request.POST.get('tags_str')

            if tags_str:
                tags_str = tags_str.strip(' #')
                tags_str = tags_str.replace(',', '#')
                tags_list = tags_str.split('#')

                for tag in tags_list:
                    tag = tag.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=tag)
                    if is_tag_created:
                        tag.slug = slugify(tag, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)

            return response
        else:
            return redirect('/forum/')


def tag_post(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()

    context = {
        'post_list': post_list.order_by('-pk'),
        'tag': tag,
        'categories': Category.objects.all(),
        'num_noncategory_posts': Post.objects.filter(category=None).count(),
    }

    return render(
        request,
        'forum/post_list.html',
        context,
    )


def category_post(request, slug):
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    context = {
        'post_list': post_list.order_by('-pk'),
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
