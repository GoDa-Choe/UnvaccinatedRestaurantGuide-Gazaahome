from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from corona.views import MapView, RestaurantList, RestaurantDetail

app_name = 'corona'

urlpatterns = [
    path('', MapView.as_view(), name='index'),


    path('unvaccinated_restaurant/', RestaurantList.as_view(), name='restaurant_index'),
    path('unvaccinated_restaurant/map/', MapView.as_view(), name='restaurant_map'),
    path('unvaccinated_restaurant/<int:pk>/', RestaurantDetail.as_view(), name='restaurant_detail'),

    path('unvaccinated_restaurant/<int:pk>/like_restaurant/', RestaurantDetail.as_view(), name='like_restaurant'),
    path('unvaccinated_restaurant/<int:pk>/dislike_restaurant/', RestaurantDetail.as_view(), name='dislike_restaurant'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
