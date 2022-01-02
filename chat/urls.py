from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from chat.views import TestChatView, leave

app_name = 'chat'
urlpatterns = [
    path('', TestChatView.as_view(), name='test_chat'),
    path('leave/<str:id>/', leave, name='leave'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
