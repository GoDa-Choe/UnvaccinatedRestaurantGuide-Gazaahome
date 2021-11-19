from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from beauty.views import PredictView

app_name = 'beauty'

urlpatterns = [
    path('', PredictView.as_view(), name='index'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
