from django.urls import path
from workday import views

app_name = 'workday'

urlpatterns = [

    path('<int:cal>/delete_leave/<int:pk>', views.LeaveDelete.as_view(), name='delete_leave'),
    path('<int:pk>/create_leave', views.LeaveCreate.as_view(), name='create_leave'),

    path('create_calculator/', views.CalculatorCreate.as_view(), name='create'),
    path('<int:pk>/delete_calculator', views.CalculatorDelete.as_view(), name='delete'),
    path('<int:pk>/update_calculator', views.CalculatorUpdate.as_view(), name='update'),

    path('search/', views.CalculatorSearch.as_view(), name='search'),
    path('search/<str:calculator_name>/', views.SearchedCalculatorList.as_view(), name='searched_list'),

    path('<int:pk>', views.CalculatorDetail.as_view(), name='detail'),
    path('', views.redirect_calculator, name='index'),
]
