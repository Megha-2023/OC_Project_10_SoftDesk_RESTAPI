from rest_framework import serializers
from .models import Projects
from authentication.serializers import UserSerializer


class ProjectSerializer(serializers.ModelSerializer):
    # author = serializers.SerializerMethodField()
    # contributors = serializers.SerializerMethodField()

    class Meta:
        model = Projects
        fields = ['id', 'title', 'description', 'author', 'contributors', 'type']
