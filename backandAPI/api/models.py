from django.db import models
# Create your models here.
class Address(models.Model):
      name=models.CharField(max_length=50,null=True)
      street_address = models.CharField(max_length=100,null=True)
      city = models.CharField(max_length=50,null=True)
      country = models.CharField(max_length=50,null=True)
      longitude= models.CharField(max_length=50,null=True)
      latitude= models.CharField(max_length=50,null=True)
      class Meta:
            swappable="ADDRESS_TB"

      def __str__(self):
            return f"{self.street_address}, {self.city}, {self.country}"
      
      @property
      def address(self):
            return  f"{self.street_address} {self.city} {self.country}"

      @property
      def coordinates(self):
            return[self.longitude,self.latitude]
      
      @property
      def point(self):
            return{'longitude':self.longitude,'latitude':self.latitude,'name':self.name}

      def address_update(self, new:dict):
            for k,v in new.items():
                  if hasattr(self, k):
                        self.__setattr__(k, v)
                  else:
                        print(f"Address class has not {k} attribute")
                        

class Media(models.Model):
      image = models.ImageField(upload_to='users_images',default='defaulttitle')
      class Meta:
            swappable="MEDIA_TB"

class Description(models.Model):
      description=models.TextField(max_length=300)

      class Meta:
            swappable="DESCRIPTION_TB"


class MessageArchivie(models.Model):
      description=models.TextField(max_length=300)
      sender=models.IntegerField()
      reciver=models.IntegerField()
      date = models.DateField(auto_now_add=True)