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
from projects.views import ProjectViewSet, IssueViewSet  


router = routers.DefaultRouter()
router.register('projects', ProjectViewSet, basename='projects')
router.register('issues', IssueViewSet, basename='issues')

projects_issues_get_post = IssueViewSet.as_view({'get': 'list',
                                                'post': 'create'})
projects_issues_put_delete = IssueViewSet.as_view({'put': 'update',
                                                   'delete': 'destroy'})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/', include(auth_urls.auth_urlpatterns)),
    path('api/', include(router.urls)),
    path('api/projects/<int:project_id>/issues/', projects_issues_get_post, name='project-issues-get-create'),
    path('api/projects/<int:project_id>/issues/<int:issue_id>', projects_issues_put_delete, name='project-issues-put-delete')
]
