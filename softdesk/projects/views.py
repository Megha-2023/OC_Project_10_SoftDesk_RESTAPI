from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from authentication.serializers import UserSerializer
from authentication.models import Users
from .models import Projects, Contributors
from .serializers import ProjectSerializer, ContributorSerializer
from .permissions import ProjectAuthentication


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [ProjectAuthentication]
    queryset = Projects.objects.all()
    lookup_field = 'id'

    def retrieve(self, request, id=None):
        project_user = Contributors.objects.filter(project=id, user=request.user)
        if project_user:
            queryset = Projects.objects.filter(id=id)
            serializer = ProjectSerializer(queryset, many=True)
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )
        if not project_user:
            return Response({'Error': 'You do not have access to the project'},
                            status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()
        if project.author == request.user:
            super().destroy(request, *args, **kwargs)
            return Response({
                'Message': 'Project has been deleted successfully'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'Message': 'You do not have permission to delete the project'
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get', 'post'], url_path='users')
    def get_or_add_users(self, request, id=None):
        users_role = []
        project = get_object_or_404(Projects, id=id)
        
        if request.method == 'GET':
            # Check if the logged-in user is the author or a contributor for this project
            if request.user != project.author and not project.contributors.filter(id=request.user.id).exists():
                raise PermissionDenied("You do not have permission to view the contributors of this project.")

            # Fetch all contributors related to this project
            project_contributors = project.contributors.all()

            serializer = UserSerializer(project_contributors, many=True)
            contributor_roles = Contributors.objects.filter(project=project)
            for contributor in contributor_roles:
                users_role.append(contributor.role)

            return Response({"contributors": serializer.data,
                             "roles": users_role},
                            status=status.HTTP_200_OK)
        
        elif request.method == 'POST':
            if request.user != project.author:
                raise PermissionDenied("Only author of the project can add contributors.")
            
            user_id = request.data.get('contributors')
            if not user_id:
                return Response({"Error": "User ID is required"},
                                status=status.HTTP_400_BAD_REQUEST)
            
            request.data['title'] = project.title

            user_to_add = get_object_or_404(Users, id=user_id)

            if user_to_add in project.contributors.all():
                return Response({"message": "User is already a contributor"},
                                status=status.HTTP_400_BAD_REQUEST)
            
            project.contributors.add(user_to_add, through_defaults={'role': 'Contributor'})
            serializer = ProjectSerializer(project, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'User saved successfully'},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path='users/(?P<user_id>[^/.]+)')
    def remove_users(self, request, id=None, user_id=None):
        project = get_object_or_404(Projects, id=id)

        if request.user != project.author:
            raise PermissionDenied("Only author of the project can remove contributor")
        
        user_to_remove = get_object_or_404(Users, id=user_id)
        if user_to_remove not in project.contributors.all():
            return Response({"Error": "User is not contributor of this project"},
                            status=status.HTTP_400_BAD_REQUEST)
        
        project.contributors.remove(user_to_remove)
        return Response({"message": "User removed from the project"},
                        status=status.HTTP_200_OK)
        
