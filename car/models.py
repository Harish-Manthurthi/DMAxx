from django.db import models

# Create your models here.

class CarBrand(models.Model):
    name = models.CharField(max_length=200,null=True,blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class CarModel(models.Model):
    name = models.CharField(max_length=200,null=True,blank=True)
    brand = models.ForeignKey(CarBrand,on_delete=models.CASCADE,related_name='carBrand',blank=True,null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name 

class CarTrim(models.Model):
    model = models.ForeignKey(CarModel,on_delete=models.CASCADE,related_name='carModel',null=True,blank=True)
    name = models.CharField(max_length=500,null=True,blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
