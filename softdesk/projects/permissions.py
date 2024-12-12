from rest_framework.permissions import BasePermission
from django.core.exceptions import ObjectDoesNotExist
from .models import Projects, Issues


class ProjectAuthentication(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            is_author = request.user == obj.author
            is_contributor = obj.contributors.filter(id=request.user.id).exists()
            return is_author or is_contributor

        elif request.method in ['PUT', 'DELETE']:
            return request.user == obj.author

        return request.user == obj.author


class IssueAuthentication(BasePermission):
    message = "Issue can be created/updated/deleted by project contributor"

    def has_permission(self, request, view):
        if request.method == 'POST':
            if hasattr(view, 'kwargs') and 'project_id' in view.kwargs:
                try:
                    project_id = view.kwargs['project_id']
                    project_obj = Projects.objects.get(id=project_id)
                except ObjectDoesNotExist:
                    return False
                return request.user in project_obj.contributors.all()
            return False
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return request.user in obj.project.contributors.all()
        
        elif request.method in ['PUT', 'DELETE']:
            return request.user == obj.issue_author
        
        return False

class CommentAuthentication(BasePermission):
    message = "Comments can be created by project contributor"

    def has_permission(self, request, view):
        if request.method == 'POST':
            if hasattr(view, 'kwargs') and 'issue_id' in view.kwargs:
                try:
                    issue_id = view.kwargs['issue_id']
                    issue_obj = Issues.objects.get(id=issue_id)
                    project_obj = Projects.objects.get(id=issue_obj.project.id)
                except ObjectDoesNotExist:
                    return False
                return request.user in project_obj.contributors.all()
            return False
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return request.user in obj.issue.project.contributors.all()
        
        elif request.method in ['PUT', 'DELETE']:
            return request.user == obj.comment_author
        
        return False
