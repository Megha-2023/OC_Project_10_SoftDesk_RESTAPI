from rest_framework import serializers
from .models import Users


class UserSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Users
        fields = ('id', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}



