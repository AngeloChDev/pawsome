
from django.conf import settings
from email.message import EmailMessage
import ssl
import smtplib

MOTIVATION={
      201:{'New-User':
           "Hallo %s, We give you welcome in our site"},
      202:{'New-Shelter':
           "Hallo %s, We give you welcome in our site like a shelter read terms and conditions."},
      203:{'User-New-Adoption':
           "Hello %s, We recived a request about you would like to adopt the pet %s"},
      204:{'Shelter-New-Adoption':
           "Hello %s, We recived a request of an user about adopt your pet %s answer to the user as soon as possible"},
      205:{'Shelter-New-Pet':
           "Hello %s, We seen you had upload a nw pet for the adoptions, we will send to you an other email about the vetrinary visit as soon as possible."},
      206:{'Veterinary':
           "Hello %s, The veterinary will come to you for visit the pet you upload in date %d, Please let we know if havi any problem or appointment in this date and we will move the appointment in an other day"},
      404:{'Danger':
           "Hallo %s, We seen about some one try to access in your account with invalid log voalues many time, let we know if have some problem"},
      303:{'User-Help-Request':
           "Hallo %s, We recived your message, it will be elaborate and you will reciva an answer as soon aspossible"},

}

class SendMail:
     def __init__(self) -> None:
      
          self.__sender = settings.PAWSOME_EMAIL
          self.__password = settings.PAWSOMEPY_KEY


     def send(self,reciver,code=201, info=None):
          
          subject, body = MOTIVATION[code].items()
          try:
               if code in [206, 204, 203] and info is None:
                    raise SyntaxError('Need info details')
               if info is None :
                    info=''
                  
               message = body %reciver %info
               email = EmailMessage()
               email['From'] = self.__sender
               email['To'] = reciver.email
               email['Subject'] = subject.replace('-', ' ')
               email.set_content(message)
               context = ssl.create_default_context()

               with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                    smtp.login(self.__sender, self.__password)
                    smtp.sendmail(self.__sender, reciver.email, email.as_string())
               
               return True
          except SyntaxError as e:
               print(e)
               return None

            