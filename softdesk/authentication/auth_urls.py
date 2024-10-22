from django.urls import path
from .views import UserSignupView, UserLoginView


auth_urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup_user'),
    path('login/', UserLoginView.as_view(), name='login'),
]