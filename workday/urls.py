from django.urls import path
from workday import views

app_name = 'workday'

urlpatterns = [

    # path('update_post/<int:pk>/', views.PostUpdate.as_view(), name='update'),
    path('create_calculator/', views.CalculatorCreate.as_view(), name='create'),

    # path('<int:pk>/', views.PostDetail.as_view(), name='detail'),

    # path('update_leave', views.LeaveUpdate.as_view(), name='update_leave'),
    path('<int:cal>/delete_leave/<int:pk>', views.LeaveDelete.as_view(), name='delete_leave'),
    path('<int:pk>/create_leave', views.LeaveCreate.as_view(), name='create_leave'),

    path('<int:pk>', views.CalculatorDetail.as_view(), name='detail'),
    path('', views.CalculatorList.as_view(), name='index'),
]