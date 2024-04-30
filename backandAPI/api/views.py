
from typing import Any
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from .models import  Description, Address
from .serializers import  DescriptionSerializer, AddressSerializer
from django.conf import settings
from rest_framework.permissions import AllowAny
from django.http import   HttpResponse
from rest_framework.response import Response
from rest_framework import status 
from copy import copy
import requests, folium
from geopy.geocoders import Nominatim
from .utils import coordinate



class DescriptionView(ModelViewSet):
      queryset = Description.objects.all()
      serializer_class= DescriptionSerializer
      model=Description
      permission_classes=(AllowAny,)
      
      @action(detail=False,methods=["POST"],url_path='savedescription',url_name='savedescription',name='savedescription')
      def savedescription(self, request):
            try:
                  if request.method == 'POST':
                        description = request.data['description']
                        description_obj=self.model.objects.create(description=description)
                        description_obj.save()
                        return Response(data=int(description_obj.id),status=status.HTTP_200_OK)
                  return Response(data=None)
            except Exception as e:
                  return Response(data={'response':f'error{e}'},status=status.HTTP_400_BAD_REQUEST)
      
      @action(detail=True,methods=["GET"],url_path='getdescription',url_name='getdescription',name='getdescription')
      def getdescription(self,request,pk):
            try:
                  description=self.get_queryset().filter(id=int(pk))
                  s=self.serializer_class(data=description,many=True)
                  s.is_valid()
                  return Response(data=s.data[0],status=status.HTTP_200_OK)
            except Exception as e:
                  return Response(data={'response':f'error{e}'},status=status.HTTP_400_BAD_REQUEST)
      
      @action(detail=True,methods=["POST"],url_path='updatedescription',url_name='updatedescription',name='updatedescription')
      def updatedescription(self, request, pk):
            try:
                  if request.method == 'POST':
                        description_obj=self.get_queryset().filter(id=int(pk))[0]
                        description_obj.description=request.data['description']
                        description_obj.save()
                        return Response(data=description_obj.id,status=status.HTTP_200_OK)
                  pass
            except Exception as e:
                  return Response(data={'response':f'error{e}'},status=status.HTTP_400_BAD_REQUEST)
      
      @action(detail=True,methods=["POST"],url_path='deletedescription',url_name='deletedescription',name='deletedescription')
      def deletedescription(self,request,  pk):
            try:
                  description=self.queryset.filter(id=pk).first()
                  description.delete()
                  return HttpResponse(data={'response':'ok'})
            except Exception as e:
                  return Response(data={'response':f'error{e}','obj_id':None},status=status.HTTP_400_BAD_REQUEST)


class AddressView(ModelViewSet):
      queryset = Address.objects.all()
      serializer_class= AddressSerializer
      permission_classes=(AllowAny,)
      model=Address

      @action(detail=False,methods=["POST"],url_path='dela',url_name='dela',name='dela')
      def dela(self, request, **k):
            
            return Response(data={'':''},status=status.HTTP_200_OK)

      @action(detail=False,methods=["POST"],url_path='saveaddress',url_name='saveaddress',name='saveaddress')
      def saveaddress(self, request, **k):
            try:
                  if request.method == 'POST':
                        data=request.data
                        place=' '.join([data['street_address'],data['city'],data['country']])
                        loc = Nominatim(user_agent="Geopy Library")
                        coord = coordinate(place)
                        s=self.serializer_class(data=data)
                        s.is_valid()
                        ad=s.create(s.data)
                        ad.save()
                        ad.longitude=coord['longitude']
                        ad.latitude=coord['latitude']
                        ad.save()
                        return Response(data=ad.id,status=status.HTTP_200_OK)
                  raise Exception
            except Exception as e:
                  return Response(data=0,status=status.HTTP_400_BAD_REQUEST)

      @action(detail=True,methods=["GET"],url_path='getaddress',url_name='getaddress',name='getaddress')
      def getaddress(self,request,pk):
            try:
                  if request.method == 'GET':
                        addr=self.get_queryset().filter(id=int(pk)).first()
                        a=dict(copy(vars(addr)))
                        s=self.serializer_class(data=a,many=False)
                        s.is_valid()
                        return Response(data={'address':s.data},status=status.HTTP_200_OK)
                  else:
                        return Response(data={'address':''},status=status.HTTP_405_METHOD_NOT_ALLOWED)
            except Exception as e:
                  return Response(data={'address':f'error{e}'},status=status.HTTP_400_BAD_REQUEST)

      @action(detail=False,methods=["GET"],url_path='getstreetaddress',url_name='getstreetaddress',name='getstreetaddress')
      def getstreetaddress(self, request):
            coordinate= request.data['address'].split('end')
            coord_tuple = [reversed(tuple(i.split(','))) for i in coordinate ]
            
            link=settings.LINK_GET_DIRECTION + f"&start={','.join(coord_tuple[0])}&end={','.join(coord_tuple[1])}".replace(" ", "")
            headers = {
                  'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
            }

            res= requests.get(link, headers)
            way=res.json()
            
            street=folium.PolyLine(locations=[tuple(reversed(c)) for c in way['features'][0]['geometry']['coordinates']],color='blue')

            return Response(data={'address':street.locations})

      @action(detail=True,methods=["PUT"],url_path='updateaddress',url_name='updateaddress',name='updateaddress')
      def updateaddress(self, request, pk):
            
            try:
                  if request.method == 'POST':
                        addr=self.get_queryset().filter(id=int(pk))[0] 
                        data=request.data
                        place=f"{data['street_address']}, {data['city']}, {data['country']}"
                        if place==addr.__str__():
                              return Response(data=addr.id)
                        loc = Nominatim(user_agent="Geopy Library")
                        coord = loc.geocode(place)
                        coord=coordinate(place)
                        addr.longitude =coord['longitude']
                        addr.latitude=coord['latitude']
                        #addr.address_update(data)
                        print(data)
                        for k,v in data.items():
                              if hasattr(addr, k):
                                    addr.__setattr__(k, v)
                              else:
                                    print(f"Address class has not {k} attribute")
                        addr.save()
                        return Response(data=addr.id,status=status.HTTP_200_OK)
                  pass
            except Exception as e:
                  return Response(data={'response':f'error{e}'},status=status.HTTP_400_BAD_REQUEST)
      
      @action(detail=True,methods=["POST"],url_path='deleteaddress',url_name='deleteaddress',name='deleteaddress')
      def deleteaddress(self, request, pk):
            address=self.queryset.filter(pk=pk).first().delete()
            return HttpResponse(data={'response':True})
      
      @action(detail=False,methods=["GET","POST"],url_path='fullmapaddress',url_name='fullmapaddress',name='fullmapaddress')
      def fullmapaddress(self, request):
            try:
                  
                  s=self.serializer_class(data=self.queryset,many=True)
                  s.is_valid()
                  return Response(data=s.data)#Response(data='xx.html', status=status.HTTP_200_OK)
            except Exception as e:
                  return Response(data={'address':f"{e}"}, status=status.HTTP_404_NOT_FOUND)


class Message(ModelViewSet):
      serializer_class = AddressSerializer
      queryset = Address.objects.all()
      permission_classes = (AllowAny, )
      #(?P<pk>[^/.]+)/
      @action(detail=False,methods=["POST"],url_path='sendmessage',url_name='sendmessage',name='sendmessage')
      def sendmessage(self, request):
            if request.method.POST:
                  sended=settings.EMAIL_SENDER.send(reciver=request.data['reciver'],code=request.data['code'])
                  return Response(data={'':''})

     # @action(detail=True,methods=["GET"],url_path='(?P<sender>[^/.]+)/getmessage',url_name='getmessage',name='getmessage')
     # def getmessage(self, request, pk):
     #       pass
#
     # @action(detail=True,methods=["GET"],url_path='listmessage',url_name='listmessage',name='listmessage')
     # def listmessage(self, request, pk):
     #       recived_list=self.get_queryset().filter(reciver=int(pk)).values_list('sender',flat=True)
     #       pass
#
     # @action(detail=True,methods=["DELETE"],url_path='(?P<message>[^/.]+)/deletemessage',url_name='deletemessage',name='deletemessage')
     # def deletemessage(self, request, pk):
     #       pass
#
     # @action(detail=True,methods=["DELETE"],url_path='deleteallmessage',url_name='deleteallmessage',name='deleteallmessage')
     # def deleteallmessage(self, request, pk):
     #       pass