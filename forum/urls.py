from django.urls import path
from forum import views

urlpatterns = [
    path('tag/<str:slug>/', views.tag_post, name='tag_post'),
    path('category/<str:slug>/', views.category_post, name='category_post'),

    path('update_post/<int:pk>/', views.PostUpdate.as_view(), name='update'),
    path('create_post/', views.PostCreate.as_view(), name='create'),

    path('<int:pk>/', views.PostDetail.as_view(), name='detail'),
    path('', views.PostList.as_view(), name='index')
]
