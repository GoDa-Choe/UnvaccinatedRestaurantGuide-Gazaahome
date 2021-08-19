from django.urls import path
from troop_review import views

app_name = 'troop_review'

urlpatterns = [
    # path('tag/<str:slug>/', views.tag_post, name='tag_post'),
    #
    # path('likes/', views.LikesPostList.as_view(), name='likes_post'),
    # path('popular/', views.PopularPostList.as_view(), name='popular_post'),
    # path('category/<str:slug>/', views.CategoryPostList.as_view(), name='category_post'),
    #
    # path('delete_post/<int:pk>/', views.PostDelete.as_view(), name='delete'),
    # path('update_post/<int:pk>/', views.PostUpdate.as_view(), name='update'),
    # path('create_post/', views.PostCreate.as_view(), name='create'),
    #
    # path('like_post/<int:pk>', views.like, name='like'),
    #
    # path('delete_comment/<int:pk>/', views.delete_comment, name='comment_delete'),
    # path('update_comment/<int:pk>/', views.CommentUpdate.as_view(), name='comment_update'),
    # path('<int:pk>/new_comment/', views.new_comment, name='comment_create'),
    # path('<int:pk>/', views.PostDetail.as_view(), name='detail'),

    path('<int:troop_pk>/like_post/<int:pk>', views.like, name='like_review'),

    path('<int:troop_pk>/delete_review/<int:pk>/', views.DeleteReview.as_view(), name='delete_review'),
    path('<int:troop_pk>/update_review/<int:pk>/', views.UpdateReview.as_view(), name='update_review'),
    path('<int:pk>/create_review/', views.CreateReview.as_view(), name='create_review'),

    path('create_troop/', views.CreateTroop.as_view(), name='create_troop'),

    path('<int:pk>/', views.TroopDetail.as_view(), name='detail'),
    path('', views.TroopList.as_view(), name='index')
]
