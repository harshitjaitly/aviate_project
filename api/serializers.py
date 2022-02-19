from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer) :

    class Meta :

        model = Profile
        fields = [
            "id",
            "name",
            "age",
            "contact",
            "resume",
            "password"
                ]

        extra_kwargs = {'password': {'write_only': True}}

class ResumeSerializer(serializers.ModelSerializer) :

    class Meta :

        model = Profile
        fields = [
            "id",
            "resume",
            "prev_resume_list"
                ]

class SuperSerializer(serializers.ModelSerializer) :

    class Meta :

        model = Profile
        fields = '__all__'
