from django.urls import path
from troop_review import views

app_name = 'troop_review'

urlpatterns = [
    path('<int:troop_pk>/like_post/<int:pk>', views.like, name='like_review'),

    path('<int:troop_pk>/delete_review/<int:pk>/', views.DeleteReview.as_view(), name='delete_review'),
    path('<int:troop_pk>/update_review/<int:pk>/', views.UpdateReview.as_view(), name='update_review'),
    path('<int:pk>/create_review/', views.CreateReview.as_view(), name='create_review'),

    path('create_troop/', views.CreateTroop.as_view(), name='create_troop'),

    path('<int:pk>/', views.TroopDetail.as_view(), name='detail'),
    path('', views.TroopList.as_view(), name='index')
]
