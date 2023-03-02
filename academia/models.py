# Stdlib Imports
import uuid

# Django Imports
from django.db import models


class Country(models.Model):
    """
    Defines the schema for academia_country table in the database.

    Fields:
        - id (int): the object unique uuid
        - name (str): the name of country
        - continent (str): what continent is this country for?
        - country_code (str): what is the code for this country? e.g NG
        - schools (m2m): many to many relationship to the academia_school_country table
    """

    CHOICES = (
        ("Asia", "Asia"),
        ("Africa", "Africa"),
        ("Europe", "Europe"),
        ("Australia", "Australia"),
        ("Antartica", "Antartica"),
        ("North America", "North America"),
        ("South America", "South America"),
    )

    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    name = models.CharField(
        max_length=500,
        null=False,
        blank=True,
        help_text="What's the name of this country?",
    )
    continent = models.CharField(
        max_length=500,
        choices=CHOICES,
        null=False,
        blank=True,
        help_text="What continent is this country in?",
    )
    country_code = models.CharField(
        max_length=50,
        null=False,
        blank=True,
        help_text="The country name code in uppercase only, e.g NG.",
    )
    schools = models.ManyToManyField(
        "School",
        blank=True,
        related_name="country_schools",
        editable=False
    )

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self) -> str:
        return self.name


class School(models.Model):
    """
    Defines the schema for academia_school table in the database.

    Fields:
        - id (int): the object unique uuid
        - listed (bool): indicate if the school is no longer valid and will not be returned in API calls (defaults to True)
        - type (str): the type of higher institution
        - name (str): the name of school
        - code (str): the associated school short code. e.g UNIZIK
        - founded (int): what year was this school located?
        - address (str): where is this school located?
        - ownership (str): the owernship status of this institution (public or private)
        - owned_by (str): if it is public, is it owned by federal, or state?
        - website (url): the official website of this institution
        - logo (url): the official logo of this insitution
        - country (fk): foreign key relationship to the acamedia_country_schools table
        - faculties (m2m): many to many relationship to the acamedia_faculty table
        - departments (m2m): many to many relationship to the academia_department table
    """

    CHOICES = (
        ("University", "University"),
        ("Polytechnic", "Polytechnic"),
        ("Monotechnic", "Monotechnic"),
        ("College", "College"),
    )

    OWNERSHIP = (
        ("Public", "Public"),
        ("Private", "Private"),
    )

    OWNED_BY = (
        ("Private", "Private"),
        ("Federal", "Federal"),
        ("State", "State"),
    )

    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    listed = models.BooleanField(
        default=True,
        help_text="Tick to indicate no longer valid and will not be returned in API calls.",
    )
    type = models.CharField(
        max_length=20,
        blank=False,
        choices=CHOICES,
        help_text="The type of higher intitution.",
    )
    name = models.CharField(
        max_length=500,
        null=False,
        blank=False,
        help_text="The name of the school.",
    )
    code = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        help_text="The asociated school short code, e.g Unizik.",
    )
    founded = models.IntegerField(
        null=True,
        blank=False,
        default="0000",
        help_text="What year was this school founded?",
    )
    address = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        help_text="Where's this school located?",
    )
    ownership = models.CharField(
        max_length=20,
        blank=False,
        choices=OWNERSHIP,
        help_text="The ownership status of this intitution, is it public or private?",
        default="None",
    )
    owned_by = models.CharField(
        max_length=20,
        blank=False,
        choices=OWNED_BY,
        help_text="If it's a Public intitution, is it federal owned or state owned?",
        default="None",
    )
    website = models.URLField(
        max_length=50,
        null=True,
        blank=True,
        help_text="The website of this institution",
    )
    logo = models.ImageField(
        null=True,
        blank=False,
        help_text="The logo of this institution",
        default="logo.png",
    )
    country = models.ForeignKey(
        Country,
        blank=False,
        related_name="school_country",
        on_delete=models.DO_NOTHING,
    )
    faculties = models.ManyToManyField(
        "Faculty", blank=True, related_name="child_faculties", editable=False
    )
    departments = models.ManyToManyField(
        "Department",
        blank=True,
        related_name="child_departments",
        editable=False,
    )

    class Meta:
        verbose_name_plural = "Schools"

    def __str__(self) -> str:
        return self.name


class Faculty(models.Model):
    """
    Defines the schema for academia_faculty table in the database.

    Fields:
        - id (int): the object unique uuid
        - school (fk): foreign key relationship to the academia_school table
        - name (str): the name of faculty
        - department (m2m): many to many relationship to the academia_faculty_departments table
    """

    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="faculty_school",
    )
    name = models.CharField(
        max_length=500,
        null=False,
        blank=False,
        help_text="The name of the Faculty",
    )
    departments = models.ManyToManyField(
        "Department",
        blank=True,
        related_name="faculty_departments",
        editable=False,
    )

    class Meta:
        verbose_name_plural = "Faculties"

    def __str__(self):
        return str(self.name)


class Department(models.Model):
    """
    Defines the schema for academia_department table in the database.

    Fields:
        - id (int): the object unique uuid
        - school (fk): foreign key relationship to the academia_school table
        - faculty (fk): foreign key relationship to the academia_faculty table
        - name (str): the name of department
        - degree (m2m): many to many relationship to the academia_degree table
        - duration (str): the number of years it takes to graduate from this department
        - code (str): the associated department code
    """

    CHOICES = (
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
        ("6", "6"),
        ("7", "7"),
        ("8", "8"),
        ("9", "9"),
        ("10", "10"),
    )

    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="department_school",
    )
    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="department_faculty",
    )
    name = models.CharField(
        max_length=500,
        null=False,
        blank=True,
        help_text="The name of the department",
    )
    degree = models.ForeignKey(
        "Degree",
        blank=False,
        default='',
        on_delete=models.CASCADE,
        help_text="The type of degree offered by this department.",
    )
    duration = models.CharField(
        max_length=10,
        null=False,
        blank=True,
        choices=CHOICES,
        help_text="The number of years it takes to graduate from this department ",
    )
    code = models.CharField(
        max_length=50,
        null=False,
        blank=True,
        help_text="The associated department code, like ECE",
    )

    class Meta:
        verbose_name_plural = "Departments"

    def __str__(self) -> str:
        return self.name


class Degree(models.Model):
    """
    Defines the schema for academia_degree table in the database.

    Fields:
        - id (int): the object unique uuid
        - name (str): the name of degree
        - code (str): the associated degree code
    """

    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    name = models.CharField(
        max_length=500,
        null=False,
        blank=True,
        help_text="The name of this degree",
    )
    code = models.CharField(
        max_length=50,
        null=False,
        blank=True,
        help_text="The associated degree code, like B.Sc",
    )

    class Meta:
        verbose_name_plural = "Degrees"

    def __str__(self) -> str:
        return self.name
