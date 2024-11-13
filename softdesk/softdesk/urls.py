"""
URL configuration for softdesk project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from authentication import auth_urls
from projects.views import ProjectViewSet  # , ProjectContributorsAPIView


router = routers.DefaultRouter()
router.register('projects', ProjectViewSet, basename='projects')

#projects_users = ProjectViewSet.as_view({'get': 'get_users',
#                                         'post': 'add_user'})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/', include(auth_urls.auth_urlpatterns)),
    path('api/', include(router.urls)),
    # path('api/projects/<int:id>/users/', projects_users, name='project-users')
]
