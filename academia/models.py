# Stdlib Imports
import uuid

# Django Imports
from django.db import models
from django.db.models import Index
from django.core.exceptions import ValidationError

# Third Party Imports
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField
from rest_framework_api_key.models import APIKey


class Client(models.Model):
    """
    Defines the schema for client table in the database.

    Fields:
        - id (uuid): The client unique uuid4 identifier.
        - name (str): The client name.
        - email (str): The client email address.
        - is_verified (bool): Is the client verified?
        - client_type (str): Is the client a developer or an organisation?
        - date_created (datetime): The date and time object was created.
        - date_modified (datetime): The data and time object was modified.
    """

    class ClientTypes(models.Choices):
        DEVELOPER = "developer"
        ORGANISATION = "organisation"

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    is_verified = models.BooleanField(default=False)
    client_type = models.CharField(choices=ClientTypes.choices, max_length=25)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "clients"
        indexes = [models.Index(fields=["id", "email", "client_type"])]

    def __str__(self) -> str:
        return f"Client: {self.name}"

class ClientAPIKey(APIKey):
    """
    Defines the clients_apikey table in the database.

    Fields:
        - *: inherits apikey from rest_framework_api_key
        - client (o2o): A one-to-one relationship to the client.
        - scope (str): The unique name that'll be used to rate api key
        - rate (bigint): The number of requests to be made per hour.
    """

    client = models.OneToOneField(
        Client, on_delete=models.CASCADE, related_name="api_key"
    )
    scope = models.SlugField(
        unique=True, max_length=100, blank=True, editable=False
    )
    rate = models.BigIntegerField(
        default=60, help_text="Default throttle rate for requests per hour."
    )
    
    class Meta:
        db_table = "clients_apikey"
        verbose_name = "Clients API Key"
        verbose_name_plural = "Clients API Key(s)"

    def __str__(self) -> str:
        return f"Client API Key: {self.name}"

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
        "School", blank=True, related_name="country_schools", editable=False
    )

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self) -> str:
        return self.name

class AdmissionRequirement(models.Model):
    program = models.ForeignKey('Programme', on_delete=models.CASCADE)
    requirement = models.CharField(max_length=10000)

    def __str__(self):
        return f"{self.program} Requirement"

class School(models.Model):
    """
    Defines the schema for academia_school table in the database.

    Fields:
        - id (int): the object unique uuid
        - listed (bool): indicate if the school is no longer valid and
            will not be returned in API calls (defaults to True)
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
    unlisted = models.BooleanField(
        default=True,
        help_text="Tick to indicate no longer valid and this school will not be returned in API Response, untick to include in API Response",  # noqa
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
    logo = CloudinaryField(
        "univast-school-logos",
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
    ranking = models.ManyToManyField(
        'Ranking', 
        blank=True, 
        related_name='school_ranking',
    )
    
    academic_sessions = models.ManyToManyField("AcademicSession", blank=True, related_name="all_school_academic_sessions")

    @property
    def current_academic_session(self):
        return self.academic_sessions.filter(is_current_session=True, school=self).first()

    class Meta:
        verbose_name_plural = "Schools"
        indexes = [
            Index(
                fields=[
                    "name",
                    "code",
                    "country",
                    "type",
                    "founded",
                    "ownership",
                    "owned_by",
                    "address",
                    "website",
                    "id",
                ]
            ),
        ]

    def __str__(self) -> str:
        return self.name + " - " + self.country.name

class AcademicSession(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="school_academic_sessions")
    programme = models.ForeignKey("Programme", on_delete=models.CASCADE, related_name="program_academic_sessions", default="0")
    start_date = models.DateField()
    end_date = models.DateField()
    is_current_session = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_current_session:
            AcademicSession.objects.filter(school=self.school, programme=self.programme).update(is_current_session=False)
        super(AcademicSession, self).save(*args, **kwargs)

    def clean(self):
        if self.is_current_session:
            if AcademicSession.objects.filter(school=self.school, programme=self.programme, is_current_session=True).exclude(pk=self.pk).exists():
                raise ValidationError("There can be only one current session per school.")
            
    @property
    def representation(self):
        return f"{self.start_date.year}/{self.end_date.year}"

    def __str__(self):
        return f"{self.school.name} - {self.start_date.year}-{self.end_date.year}"

class Semester(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="semesters")
    academic_session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, related_name='semesters')
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    is_current_semester = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.academic_session} - {self.name}"
    
    def save(self, *args, **kwargs):
        if self.is_current_semester:
            Semester.objects.filter(school=self.school, is_current_semester=True).update(is_current_semester=False)
        super(Semester, self).save(*args, **kwargs)
    
    def clean(self):
        if self.is_current_semester:
            if Semester.objects.filter(school=self.school, is_current_semester=True).exclude(pk=self.pk).exists():
                raise ValidationError("There can be only one current semester per school.")

class AcademicCalendar(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="calendar_events", null=False, blank=False)
    academic_session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, related_name='calendar_events', null=False, blank=False)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='calendar_events', null=False, blank=False)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=True, blank=True)
    event_description = RichTextField(null=True, blank=True)
    event_title = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return f"{self.event_title} for {self.academic_session} - {self.event_date}"

    class Meta:
        ordering = ['-end_date']

class Programme(models.Model):
    parent_programme = models.ForeignKey("self", on_delete=models.CASCADE, related_name="child_programmes", null=True, blank=True)
    name = models.CharField(max_length=200)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    description = RichTextField(null=True, blank=True)
    duration = models.PositiveIntegerField()  # Duration in years
    degree_type = models.CharField(max_length=100)
    prerequisites = RichTextField(null=True, blank=True)

    def __str__(self):
        return self.name + " - " + self.school.name

class Faculty(models.Model):
    """
    Defines the schema for academia_faculty table in the database.

    Fields:
        - id (int): the object unique uuid
        - school (fk): foreign key relationship to the academia_school table
        - name (str): the name of faculty
        - department (m2m): many to many relationship to the
            academia_faculty_departments table
    """

    id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False,
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
    programme = models.ManyToManyField(
        "Programme",
        blank=True,
        related_name="faculty_programmes",
        editable=True,
    )

    class Meta:
        verbose_name_plural = "Faculties"
        indexes = [
            Index(fields=["school", "name", "id"]),
        ]

    def __str__(self):
        return str(self.name) + " - " + str(self.school)

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
        default="",
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
    programme = models.ManyToManyField(
        "Programme",
        blank=True,
        related_name="department_programmes",
        editable=True,
    )

    class Meta:
        verbose_name_plural = "Departments"
        indexes = [
            Index(
                fields=[
                    "id",
                    "name",
                    "degree",
                ]
            )
        ]

    def __str__(self) -> str:
        return self.name + " - " + self.faculty.name + " - " + self.school.name

class Course(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def clean(self):
        existing_course_with_same_code = Course.objects.filter(code=self.code, school=self.school).exclude(pk=self.pk)
        if existing_course_with_same_code.exists():
            raise ValidationError("A course with the same code already exists.")

    def save(self, *args, **kwargs):
        self.clean()
        super(Course, self).save(*args, **kwargs)

class LectureTimetable(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    academic_session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    level = models.PositiveIntegerField(choices=Department.CHOICES)
    
    DAY_CHOICES = (
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
        ("Sunday", "Sunday"),
    )

    days = models.CharField(max_length=20, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    courses = models.ManyToManyField(Course, blank=True)

    class Meta:
        verbose_name_plural = "Lecture Timetables"

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
        return self.name + " - " + self.code

class AccreditationBody(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name

class Accreditation(models.Model):
    institution = models.ForeignKey(School, on_delete=models.CASCADE)
    body = models.ForeignKey(AccreditationBody, on_delete=models.CASCADE)
    date_issued = models.DateField()

    def __str__(self):
        return f"{self.institution} - {self.body}"

class Ranking(models.Model):
    institution = models.ForeignKey(School, on_delete=models.CASCADE, related_name='rankings')
    rank = models.PositiveIntegerField()
    organization = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.institution} - {self.rank}"