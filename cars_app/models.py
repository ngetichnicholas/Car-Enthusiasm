from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxLengthValidator,MinLengthValidator
from django.db.models.deletion import CASCADE
from location_field.models.plain import PlainLocationField

# Create your models here.
class User(AbstractUser):
    full_name = models.CharField(max_length=60)
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True)
    profile_picture = models.ImageField(upload_to='profiles')
    phone = models.CharField(max_length=13, null=True,blank=True, validators=[MinLengthValidator(10),MaxLengthValidator(13)])

    def save_user(self):
        self.save()

    def delete_user(self):
        self.delete()

    def __str__(self):
        return self.username
"""
An entry involves the following; car make, model, year, a few images of the car, and a map location
 for a showroom location where they take their car on weekends to display
"""

from django.contrib.gis.db import models as gis_models

class Car(models.Model):
    car_make = models.CharField(max_length=50)
    model = models.CharField(max_length=30)
    year_manufactured = models.DateTimeField()
    image_1 = models.ImageField(upload_to='cars')
    image_2 = models.ImageField(upload_to='cars')
    image_3 = models.ImageField(upload_to='cars')
    image_4 = models.ImageField(upload_to='cars')
    city = models.CharField(max_length=255)
    car_location = PlainLocationField(based_fields=['city'], zoom=7)

    def save_car(self):
        self.save()

    def delete_car(self):
        self.delete()

    @classmethod
    def search_cars(cls, car):
        return cls.objects.filter(model__icontains=car).all()

    def __str__(self):
        return self.car_make

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp',)
    
class Contact(models.Model):
    name = models.CharField(max_length = 30)
    email = models.EmailField()
    message = models.TextField()

    def save_contact(self):
        self.save()

    def delete_contact(self):
        self.delete()

    def __str__(self):
        return self.name
    
    @classmethod
    def update_contact(cls, id ,name,email ,message):
        update = cls.objects.filter(id = id).update(name = name,email = email,message=message)
        return update