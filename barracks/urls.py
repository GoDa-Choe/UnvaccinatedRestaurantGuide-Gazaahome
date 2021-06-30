from django.urls import path
from barracks import views

app_name = 'barracks'

urlpatterns = [

    path('', views.BarracksList.as_view(), name="barracks_list"),

    # path('create/', views.CreateBarracks.as_view(), name="create_barracks"),
    # path('delete/', views.DeleteBarracks.as_view(), name="delete_barracks"),
    #
    # path('<int:pk>/', views.BarracksDetail.as_view(), name="barracks_detail"),
    # path('<int:pk>/invite/', views.InviteToBarracks.as_view(), name="invite_to_barracks"),
    # path('<int:pk>/transfer/', views.TransferToBarracks.as_view(), name="transfer_to_barracks"),
    # path('<int:pk>/quit/', views.QuitBarracks.as_view(), name="quit_barracks"),
]
