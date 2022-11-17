import uuid
from django.db import models

# Create your models here.

class Country(models.Model):
    
    CHOICES = (
        ('Asia', 'Asia'),
        ('Africa', 'Africa'),
        ('Europe', 'Europe'),
        ('Australia', 'Australia'),
        ('Antartica', 'Antartica'),
        ('North America', 'North America'),
        ('South America', 'South America'),
    )
    
    id = models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=500, null=False, blank=True, help_text="What's the name of this country?")
    continent = models.CharField(max_length=500, choices=CHOICES, null=False, blank=True, help_text="What continent is this country in?")
    country_code = models.CharField(max_length=50, null=False, blank=True, help_text="The country name code, e.g NG.")
    
    class Meta:
        verbose_name_plural = "Countries"
    
    def __str__(self):
        return str(self.name)
    

class School(models.Model):
    
    CHOICES = (
        ('university', 'university'),
        ('polytechnic', 'polytechnic'),
        ('monotechnic', 'monotechnic'),
        ('college', 'college'),
    )
    
    id = models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)
    listed = models.BooleanField(default=True, help_text="Tick to indicate no longer valid and will not be returned in API calls.")
    type = models.CharField(max_length=20, choices=CHOICES, help_text="The type of higher intitution.")
    name = models.CharField(max_length=500, null=False, blank=True, help_text="The name of the school.")
    code = models.CharField(max_length=50, null=False, blank=True, help_text="The asociated school short code, e.g Unizik.")
    country = models.ManyToManyField(Country, blank=True, related_name="school_country")
    faculties = models.ManyToManyField('Faculty', blank=True, related_name="child_faculties")
    departments = models.ManyToManyField('Department', blank=True, related_name="child_departments")
    
    class Meta:
        verbose_name_plural = "Schools"
    
    def __str__(self):
        return str(self.name)
    
class Faculty(models.Model):

    id = models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=False, blank=False, related_name="faculty_school")
    name = models.CharField(max_length=500, null=False, blank=False, help_text="The name of the Faculty")
    departments = models.ManyToManyField('Department', blank=True, related_name="faculty_departments")
    
    class Meta:
        verbose_name_plural = "Faculties"
    
    def __str__(self):
        return str(self.name)
    

class Department(models.Model):
    
    id = models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=False, blank=False, related_name="department_school")
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=False, blank=False, related_name="department_faculty")
    name = models.CharField(max_length=500, null=False, blank=True, help_text="The name of the department")
    degree = models.CharField(max_length=500, null=False, blank=True, help_text="The type of degree offered by this department.")
    duration = models.IntegerField(null=False, blank=True, help_text="The duration taken to graduate from this department ")
    code = models.CharField(max_length=50, null=False, blank=True, help_text="The associated department code, like ECE")
    
    class Meta:
        verbose_name_plural = "Departments"
    
    def __str__(self):
        return str(self.name)