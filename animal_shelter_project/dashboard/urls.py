from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'dashboard'

urlpatterns =[
    path('dashboard/', dashboard_view, name='dashboard'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # added by mohsen
