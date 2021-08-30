from django.urls import path
from video_forum import views

app_name = 'video_forum'
urlpatterns = [
    # path('tag/<str:slug>/', views.tag_post, name='tag_post'),

    # path('likes/', views.LikesPostList.as_view(), name='likes_post'),
    # path('popular/', views.PopularPostList.as_view(), name='popular_post'),

    path('<int:video_pk>/like_video_comment/<int:pk>/', views.like_video_comment, name='like_video_comment'),
    path('<int:pk>/like_video/', views.like_video, name='like_video'),

    path('delete_video_comment/<int:pk>/', views.delete_video_comment, name='delete_video_comment'),
    path('update_video_comment/<int:pk>/', views.UpdateVideoComment.as_view(), name='update_video_comment'),
    path('<int:pk>/create_video_comment/', views.create_video_comment, name='create_video_comment'),

    path('<int:pk>/delete_video', views.DeleteVideo.as_view(), name='delete_video'),
    path('<int:pk>/update_video/', views.UpdateVideo.as_view(), name='update_video'),
    path('create_video/', views.CreateVideo.as_view(), name='create_video'),

    path('<int:pk>/', views.VideoDetail.as_view(), name='detail'),
    path('', views.VideoList.as_view(), name='index')
]
