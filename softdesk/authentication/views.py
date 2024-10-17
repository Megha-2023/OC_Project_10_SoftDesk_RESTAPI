from .models import Users
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework import generics
from .serializers import UserSignupSerializer, UserLoginSerializer, UserSerializer


# Create your views here.
class UserSignupView(generics.CreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSignupSerializer
    permission_classes = (AllowAny, )

   
class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user_exist = Users.objects.get(email=email)
        if user_exist:
            user = authenticate(username=user_exist.username, password=password)

            if user is not None:
                refresh_token = RefreshToken.for_user(user)
                user_serializer = UserSerializer(user)
                return Response({
                    'refresh_token': str(refresh_token),
                    'access': str(refresh_token.access_token),
                    'user': user_serializer.data
                    }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'detail': 'Invalid Credentials',
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                    'detail': 'User does not exist',
                }, status=status.HTTP_404_NOT_FOUND)
