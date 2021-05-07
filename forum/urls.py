from django.urls import path
from forum import views

urlpatterns = [
    path('<int:pk>/', views.detail, name='detail'),
    path('', views.PostList.as_view(), name='index')
]
