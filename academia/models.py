from django.db import models

# Create your models here.

class Country(models.Model):
    name = models.CharField(max_length=500, null=False, blank=True)
    continent = models.CharField(max_length=500, null=False, blank=True)
    country_code = models.CharField(max_length=50, null=False, blank=True)   
    

class Schools(models.Model):
    
    CHOICES = (
        ('university', 'university'),
        ('polytechnic', 'polytechnic'),
        ('monotechnic', 'monotechnic'),
        ('college', 'college'),
    )
    
    type = models.CharField(max_length=20, choices=CHOICES)
    code = models.CharField(max_length=50, null=False, blank=True)
    name = models.CharField(max_length=500, null=False, blank=True)
    listed = models.BooleanField(default=True, help_text="Tick to indicate no longer valid")
    
class Faculties(models.Model):
    
    school = models.ForeignKey(Schools, on_delete=models.CASCADE, null=False, blank=True)
    name = models.CharField(max_length=500, null=False, blank=True)

class Departments(models.Models):
    
    faculty = models.ForeignKey(Faculties, on_delete=models.CASCADE, null=False, blank=True)
    name = models.CharField(max_length=500, null=False, blank=True)
    degree = models.CharField(max_length=500, null=False, blank=True)