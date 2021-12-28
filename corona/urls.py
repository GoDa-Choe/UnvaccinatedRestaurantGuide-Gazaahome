from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from django.views.generic import RedirectView

from corona.views import MapView, SearchedMapView
from corona.views import RestaurantList, PopularRestaurantList, AvailableRestaurantList, UnavailableRestaurantList, \
    ConfirmRequiredRestaurantList, SearchedRestaurantList
from corona.views import RestaurantDetail
from corona.views import CreateRestaurant, UpdateRestaurant
from corona.views import RestaurantList, RestaurantDetail, CreateRestaurant, UpdateRestaurant
from corona.views import like_restaurant, dislike_restaurant
from corona.views import create_restaurant_comment, delete_restaurant_comment, UpdateRestaurantComment
from corona.views import like_restaurant_comment
from corona.views import CreateRestaurantDeleteRequest

from corona.views import PostList, PopularPostList, CategoryPostList
from corona.views import PostDetail
from corona.views import CreatePost, UpdatePost
from corona.views import PostList, PostDetail, CreatePost, UpdatePost, DeletePost
from corona.views import like_post, dislike_post
from corona.views import create_post_comment, delete_post_comment, UpdatePostComment
from corona.views import like_post_comment

app_name = 'corona'

urlpatterns = [
    path('', RedirectView.as_view(url='/corona/unvaccinated_restaurant/'), name='index'),
    path('unvaccinated_restaurant/map/', MapView.as_view(), name='restaurant_map'),

    path('unvaccinated_restaurant/map/search/<str:search_string>/', SearchedMapView.as_view(), name='searched_restaurant_map'),

    path('unvaccinated_restaurant/', RestaurantList.as_view(), name='restaurant_index'),
    path('unvaccinated_restaurant/popular/', PopularRestaurantList.as_view(), name='popular_restaurant_index'),
    path('unvaccinated_restaurant/available/', AvailableRestaurantList.as_view(), name='available_restaurant_index'),
    path('unvaccinated_restaurant/unavailable/', UnavailableRestaurantList.as_view(),
         name='unavailable_restaurant_index'),
    path('unvaccinated_restaurant/confirm_required/', ConfirmRequiredRestaurantList.as_view(),
         name='confirm_required_restaurant_index'),

    path('unvaccinated_restaurant/search/<str:search_string>/', SearchedRestaurantList.as_view(),
         name='searched_restaurant_index'),
    # Todo

    path('unvaccinated_restaurant/create/', CreateRestaurant.as_view(), name='restaurant_create'),

    path('unvaccinated_restaurant/<int:pk>/', RestaurantDetail.as_view(), name='restaurant_detail'),
    path('unvaccinated_restaurant/<int:pk>/create_delete_request/', CreateRestaurantDeleteRequest.as_view(), name='restaurant_delete_requset'),
    path('unvaccinated_restaurant/<int:pk>/update/', UpdateRestaurant.as_view(), name='restaurant_update'),

    path('unvaccinated_restaurant/<int:pk>/like/', like_restaurant, name='like_restaurant'),
    path('unvaccinated_restaurant/<int:pk>/dislike/', dislike_restaurant, name='dislike_restaurant'),

    path('unvaccinated_restaurant/<int:pk>/comment/create/', create_restaurant_comment,
         name='create_restaurant_comment'),
    path('unvaccinated_restaurant/<int:restaurant_pk>/comment/<int:pk>/delete/', delete_restaurant_comment,
         name='delete_restaurant_comment'),
    path('unvaccinated_restaurant/<int:restaurant_pk>/comment/<int:pk>/update/', UpdateRestaurantComment.as_view(),
         name='update_restaurant_comment'),

    path('unvaccinated_restaurant/<int:restaurant_pk>/comment/<int:pk>/like/', like_restaurant_comment,
         name='like_restaurant_comment'),

    path('post/', PostList.as_view(), name='post_index'),
    path('post/category/<str:name>/', CategoryPostList.as_view(), name='category_post_index'),

    path('post/create/', CreatePost.as_view(), name='post_create'),

    path('post/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('post/<int:pk>/update/', UpdatePost.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', DeletePost.as_view(), name='post_delete'),

    path('post/<int:pk>/like/', like_post, name='like_post'),
    path('post/<int:pk>/dislike/', dislike_post, name='dislike_post'),

    path('post/<int:pk>/comment/create/', create_post_comment,
         name='create_post_comment'),
    path('post/<int:post_pk>/comment/<int:pk>/delete/', delete_post_comment,
         name='delete_post_comment'),
    path('post/<int:post_pk>/comment/<int:pk>/update/', UpdatePostComment.as_view(),
         name='update_post_comment'),

    path('post/<int:post_pk>/comment/<int:pk>/like/', like_post_comment,
         name='like_post_comment'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
