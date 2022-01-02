from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from corona_home.views import HomeView, PofileView, ContributorView, PolicyView, PrivacyView, \
    LicenseView, RobotView, GodaSoftStudioView

app_name = 'corona_home'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    # path('goda_soft_studio/', GodaSoftStudioView.as_view(), name='goda_soft_studio'),
    path('profile/', PofileView.as_view(), name='profile'),
    # path('profile/delete_account/<int:pk>/', AccountDeleteView.as_view(), name='delete_account'),

    path('contributors/', ContributorView.as_view(), name='contributor'),

    path('policy/', PolicyView.as_view(), name='policy'),
    path('policy/privacy/', PrivacyView.as_view(), name='privacy'),
    path('policy/license/', LicenseView.as_view(), name='license'),

    # path('robots.txt/', RobotView.as_view(), name='robot'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
