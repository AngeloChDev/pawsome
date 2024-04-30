from django.urls import path,include
from .views import DescriptionView, Message, AddressView
from rest_framework.routers import SimpleRouter
rout_description=SimpleRouter()
rout_description.register('description',DescriptionView,'description')
rout_address=SimpleRouter()
rout_address.register('address',AddressView,'address')
rout_message=SimpleRouter()
rout_message.register('message',Message,'message')


urlpatterns = [
    path('', include(rout_description.urls)),
    path('', include(rout_address.urls)),
    path('', include(rout_message.urls)),
    
]