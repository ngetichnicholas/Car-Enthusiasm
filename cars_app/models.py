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
class Car(models.Model):
    car_make = models.CharField(max_length=50)
    model = models.CharField(max_length=30)
    year_manufactured = models.DateTimeField()
    image_1 = models.ImageField(upload_to='cars')
    image_2 = models.ImageField(upload_to='cars')
    image_3 = models.ImageField(upload_to='cars')
    image_4 = models.ImageField(upload_to='cars')
    car_location = models.ForeignKey("Location",on_delete=CASCADE)

class Location(models.Model):
    city = models.CharField(max_length=255)
    location_point = PlainLocationField(based_fields=['city'], zoom=7)

    def save_location(self):
        self.save()

    def delete_location(self):
        self.delete()

    def __str__(self):
        return self.city

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