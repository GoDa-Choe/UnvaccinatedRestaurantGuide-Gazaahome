from django.shortcuts import redirect, get_object_or_404

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from hitcount.views import HitCountDetailView

from video_forum.forms import VideoCommentForm, VideoForm
from video_forum.models import Video, VideoTag, VideoComment, VideoCategory


class LikesVideoList(ListView):
    model = Video
    template_name = 'video_forum/index.html'
    paginate_by = 5
    context_object_name = 'video_list'

    def get_queryset(self):
        return sorted(Video.objects.all(), key=lambda video: (video.num_likes(), video.pk), reverse=True)[:20]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LikesVideoList, self).get_context_data()
        context['video_comment_form'] = VideoCommentForm
        context['num_video'] = Video.objects.count()
        context['category_list'] = VideoCategory.objects.all()

        return context


class CommentsVideoList(ListView):
    model = Video
    template_name = 'video_forum/index.html'
    paginate_by = 5
    context_object_name = 'video_list'

    def get_queryset(self):
        return sorted(Video.objects.all(), key=lambda video: (video.num_comments(), video.pk), reverse=True)[:20]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CommentsVideoList, self).get_context_data()
        context['video_comment_form'] = VideoCommentForm
        context['num_video'] = Video.objects.count()
        context['category_list'] = VideoCategory.objects.all()

        return context


class PopularVideoList(ListView):
    model = Video
    template_name = 'video_forum/index.html'
    context_object_name = 'video_list'
    paginate_by = 5

    def get_queryset(self):
        return Video.objects.order_by("-hit_count_generic__hits", '-pk')[:20]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PopularVideoList, self).get_context_data()
        context['video_comment_form'] = VideoCommentForm
        context['num_video'] = Video.objects.count()
        context['category_list'] = VideoCategory.objects.all()

        return context


class CateogryVideoList(ListView):
    model = Video
    template_name = 'video_forum/index.html'
    context_object_name = 'video_list'
    paginate_by = 5
    ordering = '-pk'

    def get_queryset(self):
        queryset = Video.objects.filter(category__name=self.kwargs['category']).order_by('-pk')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CateogryVideoList, self).get_context_data()
        context['video_comment_form'] = VideoCommentForm
        context['num_video'] = Video.objects.count()
        context['category_list'] = VideoCategory.objects.all()

        return context


class VideoList(ListView):
    model = Video
    template_name = 'video_forum/index.html'
    context_object_name = 'video_list'
    paginate_by = 5
    ordering = '-pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VideoList, self).get_context_data()
        context['video_comment_form'] = VideoCommentForm
        context['num_video'] = Video.objects.count()
        context['category_list'] = VideoCategory.objects.all()

        return context


class VideoDetail(HitCountDetailView):
    model = Video
    template_name = 'video_forum/detail.html'
    count_hit = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VideoDetail, self).get_context_data()
        context['video_comment_form'] = VideoCommentForm
        context['num_video'] = Video.objects.count()
        context['category_list'] = VideoCategory.objects.all()

        return context


class CreateVideo(LoginRequiredMixin, CreateView):
    model = Video
    form_class = VideoForm
    template_name = 'video_forum/create_video.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super(CreateVideo, self).form_valid(form)

        tags_str = self.request.POST.get('tags_str')

        if tags_str:
            tags_list = tags_str.strip(' #').replace("#", " ").split()

            for tag in tags_list:
                tag = tag.strip()
                tag, created = VideoTag.objects.get_or_create(name=tag)
                self.object.tags.add(tag)

        return response


class DeleteVideo(LoginRequiredMixin, DeleteView):
    model = Video
    template_name = 'video_forum/delete_video.html'

    def dispatch(self, request, *args, **kwargs):
        video = Video.objects.get(pk=self.kwargs['pk'])
        if video.author == self.request.user:
            return super(DeleteVideo, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super(DeleteVideo, self).get_context_data(**kwargs)
        video = Video.objects.get(pk=self.kwargs['pk'])
        context['video'] = video
        return context

    def get_success_url(self):
        return reverse_lazy('video_forum:index')


class UpdateVideo(LoginRequiredMixin, UpdateView):
    model = Video
    form_class = VideoForm
    template_name = 'video_forum/update_video.html'

    def dispatch(self, request, *args, **kwargs):
        current_video = Video.objects.get(pk=self.kwargs['pk'])

        if current_video.author == self.request.user:
            return super(UpdateVideo, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super(UpdateVideo, self).get_context_data()
        if self.object.tags.exists():
            tags_str_list = []
            for tag in self.object.tags.all():
                tags_str_list.append(tag.name)
            context['tags_str_default'] = '#' + '#'.join(tags_str_list)

        return context

    def form_valid(self, form):
        response = super(UpdateVideo, self).form_valid(form)
        self.object.tags.clear()

        tags_str = self.request.POST.get('tags_str')

        if tags_str:
            tags_list = tags_str.strip(' #').replace("#", " ").split()

            for tag in tags_list:
                tag = tag.strip()
                tag, created = VideoTag.objects.get_or_create(name=tag)
                self.object.tags.add(tag)

        return response


@require_POST
@login_required
def like_video_comment(request, video_pk, pk):
    video_comment = get_object_or_404(VideoComment, pk=pk)
    if video_comment.likes.filter(pk=request.user.pk).exists():
        video_comment.likes.remove(request.user)
    else:
        video_comment.likes.add(request.user)

    return HttpResponseRedirect(reverse('video_forum:detail', args=(video_pk,)))


@require_POST
@login_required
def like_video(request, pk):
    video = get_object_or_404(Video, pk=pk)
    if video.likes.filter(pk=request.user.pk).exists():
        video.likes.remove(request.user)
    else:
        video.likes.add(request.user)

    return HttpResponseRedirect(reverse('video_forum:detail', args=(pk,)))


class UpdateVideoComment(LoginRequiredMixin, UpdateView):
    model = VideoComment
    form_class = VideoCommentForm
    template_name = 'video_forum/update_video_comment.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user == self.get_object().author:
            return super(UpdateVideoComment, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


@login_required
def delete_video_comment(request, video_pk, pk):
    video_comment = get_object_or_404(VideoComment, pk=pk)
    video = video_comment.video
    if request.user == video_comment.author:
        video_comment.delete()
        return redirect(video.get_absolute_url())
    else:
        raise PermissionDenied


@require_POST
@login_required
def create_video_comment(request, video_pk):
    video = get_object_or_404(Video, pk=video_pk)
    video_comment_form = VideoCommentForm(request.POST)

    if video_comment_form.is_valid():
        video_comment = video_comment_form.save(commit=False)
        video_comment.video = video
        video_comment.author = request.user
        video_comment.save()

        return redirect(video_comment.get_absolute_url())
