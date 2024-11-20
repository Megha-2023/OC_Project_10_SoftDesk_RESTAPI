from rest_framework.permissions import BasePermission
from .models import Projects


class ProjectAuthentication(BasePermission):

    def has_permission(self, request, view):
        print(f"Checking general permissions: {request.user}")
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        print(f"Checking obj permission for project: {obj.id} and user:{request.user}")
        if request.method == 'GET':
            is_author = request.user == obj.author
            is_contributor = obj.contributors.filter(id=request.user.id).exists()
            print(f"is_author:{is_author}, is_contributor:{is_contributor}")
            return is_author or is_contributor

        elif request.method in ['PUT', 'DELETE']:
            return request.user == obj.author
        
        return request.user == obj.author


class IssueAuthentication(BasePermission):
    
    def has_permission(self, request, view):
        if request.method == 'POST':
            if hasattr(view, 'kwargs') and 'project_id' in view.kwargs:
                project_id = view.kwargs['project_id']
            project = Projects.objects.get(id=project_id)
            return request.user in project.contributors.all()
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return request.user in obj.project.contributors.all()
        
        elif request.method in ['PUT', 'DELETE']:
            return request.user == obj.issue_author
        
        return False
