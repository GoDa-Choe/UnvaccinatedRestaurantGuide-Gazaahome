from django.urls import path
from forum import views

urlpatterns = [
    path('tag/<str:slug>/', views.tag_post, name='tag_post'),

    path('likes/', views.LikesPostList.as_view(), name='likes_post'),
    path('popular/', views.PopularPostList.as_view(), name='popular_post'),
    path('category/<str:slug>/', views.CategoryPostList.as_view(), name='category_post'),

    path('delete_post/<int:pk>/', views.PostDelete.as_view(), name='delete'),
    path('update_post/<int:pk>/', views.PostUpdate.as_view(), name='update'),
    path('create_post/', views.PostCreate.as_view(), name='create'),

    path('like_post/<int:pk>', views.like, name='like'),

    path('delete_comment/<int:pk>/', views.delete_comment, name='comment_delete'),
    path('update_comment/<int:pk>/', views.CommentUpdate.as_view(), name='comment_update'),
    path('<int:pk>/new_comment/', views.new_comment, name='comment_create'),
    path('<int:pk>/', views.PostDetail.as_view(), name='detail'),
    path('', views.PostList.as_view(), name='index')
]
