from django.urls import path
from video_forum import views

app_name = 'video_forum'
urlpatterns = [
    path('mostlikes/', views.LikesVideoList.as_view(), name='likes_video'),
    path('mostcomments/', views.CommentsVideoList.as_view(), name='comments_video'),
    path('mostpopular/', views.PopularVideoList.as_view(), name='popular_video'),

    path('<int:video_pk>/comment/<int:pk>/like/', views.like_video_comment, name='like_video_comment'),
    path('<int:pk>/like/', views.like_video, name='like_video'),

    path('<int:video_pk>/comment/<int:pk>/delete/', views.delete_video_comment,
         name='delete_video_comment'),
    path('<int:video_pk>/comment/<int:pk>/update/', views.UpdateVideoComment.as_view(),
         name='update_video_comment'),
    path('<int:video_pk>/comment/create/', views.create_video_comment,
         name='create_video_comment'),

    path('<int:pk>/delete/', views.DeleteVideo.as_view(), name='delete_video'),
    path('<int:pk>/update/', views.UpdateVideo.as_view(), name='update_video'),
    path('create/', views.CreateVideo.as_view(), name='create_video'),

    path('<int:pk>/', views.VideoDetail.as_view(), name='detail'),

    path('', views.VideoList.as_view(), name='index'),
    path('category/<str:category>/', views.CateogryVideoList.as_view(), name='category_video')
]
