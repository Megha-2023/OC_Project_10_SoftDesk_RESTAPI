from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import Projects, Issues


class ProjectAuthentication(BasePermission):
    message = "Project can be created/updated/deleted by project contributor"

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            is_author = request.user == obj.author
            is_contributor = obj.contributors.filter(id=request.user.id).exists()
            return is_author or is_contributor

        elif request.method in ['PUT', 'DELETE']:
            return request.user == obj.author

        return False


class IssueAuthentication(BasePermission):
    # message = "Issue can be updated/deleted by author of the issue"

    def has_permission(self, request, view):
        if request.method == 'POST':
            if hasattr(view, 'kwargs') and 'project_id' in view.kwargs:
                project_id = view.kwargs['project_id']
                project_obj = get_object_or_404(Projects, id=project_id)
                return request.user in project_obj.contributors.all()
            raise PermissionDenied("Issue can be created by contributor of the project only")
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return request.user in obj.project.contributors.all()
        
        elif request.method in ['PUT', 'DELETE']:
            return request.user == obj.issue_author
        
        raise PermissionDenied("Issue can be updated/deleted by author of the issue")

class CommentAuthentication(BasePermission):
    # message = "Comments can be created by author of the issue"

    def has_permission(self, request, view):
        if request.method == 'POST':
            if hasattr(view, 'kwargs') and 'issue_id' in view.kwargs:
                issue_id = view.kwargs['issue_id']
                issue_obj = Issues.objects.get(id=issue_id)
                return request.user == issue_obj.issue_author
            return False
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return request.user in obj.issue.project.contributors.all()
        
        elif request.method in ['PUT', 'DELETE']:
            return request.user == obj.comment_author
        
        raise PermissionDenied("Comment can be updated/deleted by author of the comment")
