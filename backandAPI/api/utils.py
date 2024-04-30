from geopy.geocoders import Nominatim
import openrouteservice , folium
from openrouteservice.directions import directions
from django.conf import settings

def coordinate(addr):
      
      loc = Nominatim(user_agent="Geopy Library")

      coord = loc.geocode(addr)
      point={'longitude':coord.longitude, 'latitude':coord.latitude}
      return point


def get_street(data):
      client  =openrouteservice.Client(key=settings.GETSTREET_OPENROUTE)
      coords=[(53.599521, 10.066837),(53.594842, 10.060522)]
      m=folium.Map(location=list(reversed([53.594842, 10.060522])),width=400,height=400,tiles='cartodbpositron',zoom_start=10)
      route=directions(client,coordinates=data,format='json')
      street = folium.PolyLine(locations=[(coord) for coord in route['features'][0]['geometry']['coordinates']],color='blue')
      return f"{street}"
