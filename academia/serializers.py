# REST framework imports
from rest_framework import serializers

# Own imports
from academia.models import Country, School, Faculty, Degree, Department


class DegreeSerializer(serializers.ModelSerializer):
    """
    This seriliazer serilizes data for the Faculty database model

    :param: Request and/or object
    :return: Serilized data specified by provided fields
    """

    class Meta:
        model = Degree
        fields = [
            "id",
            "name",
        ]
        read_only_fields = fields


class CountrySerializer(serializers.ModelSerializer):
    """
    This seriliazer serilizes data for the Country database model

    :param: Request and/or object
    :return: Serilized data specified by provided fields
    """

    name = serializers.CharField(
        help_text="What is the name of this country?", required=True
    )
    country_code = serializers.CharField(
        help_text="What is the country code? E.g NG", required=True
    )

    class Meta:
        model = Country
        fields = [
            "id",
            "name",
            "country_code",
        ]


class SchoolSerializer(serializers.ModelSerializer):
    """
    This seriliazer serilizes data for the School database model

    :param: Request and/or object
    :return: Serilized data specified by provided fields
    """

    logo = serializers.SerializerMethodField(
        read_only=True, help_text="The school official logo."
    )

    class Meta:
        model = School
        fields = [
            "id",
            "type",
            "name",
            "code",
            "website",
            "logo",
            "ownership",
            "owned_by",
            "founded",
            "address",
        ]

    def get_logo(self, obj: School) -> str:
        """This method gets the logo of the school."""

        return obj.logo.url

class MiniSchoolSerializer(serializers.ModelSerializer):
    """
    This seriliazer serilizes data for the School database model

    :param: Request and/or object
    :return: Serilized data specified by provided fields
    """
    logo = serializers.SerializerMethodField(
        read_only=True, help_text="The school official logo."
    )

    class Meta:
        model = School
        fields = [
            "id",
            "name",
            "code",
            "logo"
        ]
        
    def get_logo(self, obj: School) -> str:
        """This method gets the logo of the school."""

        return obj.logo.url

class FacultySerializer(serializers.ModelSerializer):
    """
    This seriliazer serilizes data for the Faculty database model

    :param: Request and/or object
    :return: Serilized data specified by provided fields
    """
    school = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Faculty
        fields = [
            "id",
            "name",
            "school",
        ]

    def get_school(self, obj):
        """"This takes the object and returns a serialised data of its school"""

        serializer = MiniSchoolSerializer(obj.school, many=False)
        return serializer.data

class MiniFacultySerializer(serializers.ModelSerializer):
    """
    This seriliazer serilizes data for the Faculty database model

    :param: Request and/or object
    :return: Serilized data specified by provided fields
    """

    class Meta:
        model = Faculty
        fields = [
            "id",
            "name",
        ]


class DepartmentSerializer(serializers.ModelSerializer):
    """
    This seriliazer serilizes data for the Department database model

    :param: Request and/or object
    :return: Serilized data specified by provided fields
    """

    degree = DegreeSerializer(many=False, read_only=True)
    faculty = serializers.SerializerMethodField(read_only=True)
    school = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Department
        fields = ["id", "name", "code", "duration",
                  "degree", "faculty", "school"]

    def get_faculty(self, obj):
        """"This takes the object and returns a serialised data of its faculty"""

        serializer = MiniFacultySerializer(obj.faculty, many=False)
        return serializer.data

    def get_school(self, obj):
        """"This takes the object and returns a serialised data of its school"""

        serializer = MiniSchoolSerializer(obj.school, many=False)
        return serializer.data
