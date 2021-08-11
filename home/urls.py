"""gazahome URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from home import views

app_name = 'home'
urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.PofileView.as_view(), name='profile'),
    path('profile/delete_account/<int:pk>/', views.AccountDeleteView.as_view(), name='delete_account'),

    path('contributor/', views.ContributorView.as_view(), name='contributor'),

    path('policy/', views.PolicyView.as_view(), name='policy'),
    path('policy/privacy/', views.PrivacyView.as_view(), name='privacy'),
    path('policy/license/', views.LicenseView.as_view(), name='license'),

    path('robots.txt/', views.RobotView.as_view(), name='robot'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
