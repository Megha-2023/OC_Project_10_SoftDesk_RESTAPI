from django.urls import path
from .views import CreateUserAPIView

auth_urlpatterns = [
    path('signup/', CreateUserAPIView.as_view()),
]