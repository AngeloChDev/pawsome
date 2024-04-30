import requests, os
BASE_API_URL =  os.environ.get("BASE_API_URL", 'http://127.0.0.1:8001/api/')

def dispatch(key, action, obj=None, pk=None,BASE=None):
      todo=action+key
      
      method= requests.get if (action=='get' or action.startswith('get')) else requests.post
      url =f'{BASE_API_URL}{key}/{pk}/{todo}/' if pk!=None else f'{BASE_API_URL}{key}/{todo}/'
      data_dict= {key:obj} if obj is not None else obj
      if action in ('get', 'getstreet'):
            print('URLget',url)
            req= method(url, data=data_dict)
            return req.json()[key]
      elif action=='save':
            req= method(url,data=data_dict)
            return req.json()
      else:
            req= method(url,data=data_dict)
            return req.json()
      

