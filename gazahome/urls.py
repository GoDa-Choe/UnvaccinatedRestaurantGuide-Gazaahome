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
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [

    # path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    # path('bestgoda/', admin.site.urls),

    # re_path(r'^', TemplateView.as_view(url="https://godasoft-studio.github.io/"), name='maintenance'),

    path('', include('home.urls')),

    # path('forum/', include('forum.urls')),

    path('corona/', include('corona.urls')),
    path('corona/chat/', include('chat.urls')),

    # Todo
    # path('corona_home/', include('corona_home.urls')),

    path('corona/video_forum/', include('video_forum.urls')),

    # path('workday/', include('workday.urls')),
    # path('barracks/', include('barracks.urls')),
    # path('ranking/', include('rank.urls')),
    # path('troop_review/', include('troop_review.urls')),
    # path('beauty/', include('beauty.urls')),

    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('bestgoda/', admin.site.urls),

    path('accounts/', include('allauth.urls')),

    path('markdownx/', include('markdownx.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
