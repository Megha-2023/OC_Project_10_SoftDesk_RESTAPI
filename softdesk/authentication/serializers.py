from .models import Users
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """ Class to serialize and get back data from Users table"""
    class Meta:
        """ Meta class"""
        model = Users
        fields = ['id', 'first_name', 'last_name', 'email', 'username']


class UserSignupSerializer(serializers.ModelSerializer):
    """ Class to sign up new User"""
    password = serializers.CharField(min_length=8,
                                     style={'input_type': 'password'})

    class Meta:
        """ Meta class"""
        model = Users
        fields = ['first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):
        username_str = validated_data['first_name'][0] + validated_data['last_name']
        user = Users.objects.create_user(
            username=username_str,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    """ Class to authenticate user"""
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

