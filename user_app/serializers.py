from rest_framework import serializers
from .models import Student

from test_app.models import Result
from test_app.serializer import ResultAPISerializer

class StudentSerializer(serializers.ModelSerializer):
    test_results = ResultAPISerializer(many=True, read_only=True)

    class Meta:
        model = Student
        # fields = ('__all__')
        fields = (
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "slug",
            "age",
            "sex",
            "state",
            "photo",
            "email",
            "phone_number",
            "father_number",
            'test_results',  
            "created_at",
            "last_login",
        )





