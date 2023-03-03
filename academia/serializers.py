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

        request = self.context.get("request")
        logo = (
            request.scheme
            + "://"
            + request.get_host()
            + "/images/"
            + str(obj.logo)
        )
        return logo


class FacultySerializer(serializers.ModelSerializer):
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

    class Meta:
        model = Department
        fields = ["id", "name", "degree", "duration"]
