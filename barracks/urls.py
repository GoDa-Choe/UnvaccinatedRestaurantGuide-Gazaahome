from django.urls import path
from barracks import views

app_name = 'barracks'
urlpatterns = [

    path('', views.BarracksList.as_view(), name="barracks_list"),

    path('create/', views.CreateBarracks.as_view(), name="create_barracks"),

    path('delete_guest_book/<int:pk>/', views.delete_guest_book, name='guest_book_delete'),
    path('update_guest_book/<int:pk>/', views.GuestBookUpdate.as_view(), name='guest_book_update'),
    path('<int:pk>/new_guest_book/', views.new_guest_book, name='guest_book_create'),

    path('<int:pk>/', views.BarracksDetail.as_view(), name="barracks_detail"),
    path('<int:pk>/delete/', views.DeleteBarracks.as_view(), name="delete_barracks"),

    path('<int:pk>/invite/', views.CalculatorSearch.as_view(), name="search_calculator"),
    path('<int:pk>/invite/<str:calculator_name>/', views.SearchedCalculatorList.as_view(),
         name="searched_calculator_list"),
    path('<int:pk>/invite/<str:calculator_name>/send_invitation/', views.SendInvitation.as_view(),
         name="send_invitation"),
    path('<int:pk>/invite/<int:invitation_pk>/delete_invitation/', views.DeleteInvitation.as_view(),
         name="delete_invitation"),
    path('<int:pk>/invite/<str:invitation_pk>/accept_invitation/', views.AcceptInvitation.as_view(),
         name="accept_invitation"),
    path('invitation/', views.InvitationList.as_view(), name="invitation_list"),

    path('<int:pk>/transfer/', views.TransferToBarracks.as_view(), name="transfer_to_barracks"),
    path('<int:pk>/quit/', views.QuitBarracks.as_view(), name="quit_barracks"),

]
