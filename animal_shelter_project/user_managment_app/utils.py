import requests
from django.conf import settings

def dispatch(key, action, obj=None, pk=None):
      todo=action+key
      #BASE_API=settings.BASE_API
      method= requests.get if (action=='get' or action.startswith('get')) else requests.post
      url =f'http://127.0.0.1:8001/api/{key}/{pk}/{todo}/' if pk is not None else f'http://127.0.0.1:8001/api/{key}/{todo}/'
      data_dict= {key:obj} if obj is not None and not isinstance(obj, dict) else obj
      
      if action in ('get', 'getstreet'):
            req= requests.get(url,data=data_dict)
            r=req.json()
            return r[key]
      elif action=='save':
            req= requests.post( f'http://127.0.0.1:8001/api/{key}/{todo}/',data=data_dict)
            r=req.json()
            return r
      elif action=='fullmap':
            req= requests.get( f'http://127.0.0.1:8001/api/{key}/{todo}/')
            r=req.json()
            return r
      elif action=='update':
            req= requests.put( f'http://127.0.0.1:8001/api/{key}/{pk}/{todo}/',data=data_dict)
            r=req.json()
            return r
      elif action=='send':
            req= requests.post( f'http://127.0.0.1:8001/api/{key}/{todo}/',data=data_dict)
            r=req.json()
            return r
      else:
            req= requests.post(url,data=data_dict)
            r=req.json()
            return r




real_address=[
    'Altengammer Str. 2 , Lübeck , germany',
    'Reeperbahn 18,  Kiel , germany',
    'Nienstadtstraße 4,  Rendsburg, germany',
    'Marienburger Weg 14,  Hannover, germany',
    'Marienburger Weg 41,  Hannover, germany',
    'Krendelstraße 34, Isernhagen, germany',
    '15 Rue Prince Henri, Colmar Colmar-Berg, Lussemburgo',
    '27 Rue Comté Jean-Frédéric Autel, Mersch, Lussemburgo'
    'Neckarstraße 66,  Bensheim, germany',
    'David Tenierslaan 3, Kortrijk, Belgio',
    '89 Bd Montebello,  Lille, Francia',
    '2 Rue des Canonniers,  Lille, Francia',
    '1 Place François Mitterrand, Euralille, Francia',
    '79 Rue du Maréchal Foch, La Madeleine, Francia',
    

]
#def load():
#
#    from random import choice
#    password='1QAY2wsx!'
#    for i in range(1,30):
#        c=choice(real_address).split(',')
#        s=CustomUser.objects.create( username=f'A{i}',    email=f'A{i}@j.uk', first_name=f'A{i}',last_name=f'Ax{i}',street_address=c[0],city=c[1],country=c[2])
#        s.set_password(password)
#        s.is_shelter=True
#        s.save()
#        u=Shelter.objects.create(user=s,shelter_name=f'A{i}',website=f'A{i}.uk',description='skjdsfk')
#        d=u.description
#        u.description=dispatch('description','save',d)
#        u.location
#        u.save() 