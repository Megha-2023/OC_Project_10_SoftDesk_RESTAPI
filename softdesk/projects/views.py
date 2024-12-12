from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action
from authentication.serializers import UserSerializer
from authentication.models import Users
from .models import Projects, Contributors, Issues, Comments
from .serializers import ProjectSerializer, IssueSerializer, CommentSerializer
from .permissions import ProjectAuthentication, IssueAuthentication, CommentAuthentication


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

    def update(self, request, *args, **kwargs):
        partial = True
        project = self.get_object()
        serializer = self.get_serializer(project, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)

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

            contributor_id = request.data.get('contributors')
            if not contributor_id:
                return Response({"Error": "User ID is required"},
                                status=status.HTTP_400_BAD_REQUEST)

            request.data['title'] = project.title

            contributor_to_add = get_object_or_404(Users, id=contributor_id)

            if contributor_to_add in project.contributors.all():
                return Response({"message": "User is already a contributor"},
                                status=status.HTTP_400_BAD_REQUEST)

            project.contributors.add(contributor_to_add, through_defaults={'role': 'Contributor'})
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

        contributor_to_remove = get_object_or_404(Users, id=user_id)
        if contributor_to_remove not in project.contributors.all():
            return Response({"Error": "User is not contributor of this project"},
                            status=status.HTTP_400_BAD_REQUEST)

        project.contributors.remove(contributor_to_remove)
        return Response({"message": "User removed from the project"},
                        status=status.HTTP_200_OK)


class IssueViewSet(ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IssueAuthentication]
    queryset = Issues.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')

        if not Projects.objects.filter(id=project_id).exists():
            raise NotFound("Project does not exist")

        # Check if logged-in user is contributor of the project
        project = Projects.objects.get(id=project_id)
        if self.request.user not in project.contributors.all():
            raise PermissionDenied("You are not a contributor of this project")

        return self.queryset.filter(project=project_id)

    def get_object(self):
        project_id = self.kwargs.get('project_id')
        issue_id = self.kwargs.get('issue_id')
        issue_obj = Issues.objects.get(id=issue_id, project=project_id)
        return issue_obj

    def perform_create(self, serializer):
        serializer.save(issue_author=self.request.user)

    def update(self, request, *args, **kwargs):
        try:
            issue = self.get_object()
        except Issues.DoesNotExist:
            return Response({'message': "Issue number does not exist in this project"},
                            status=status.HTTP_404_NOT_FOUND)

        # Explicitly check object permission for PUT method
        self.check_object_permissions(request, issue)

        # if issue_assignee id is passed, check whether the user is in contributors list or not
        issue_assignee_id = request.data.get('issue_assignee')
        if issue_assignee_id:
            assignee_user = Users.objects.get(id=issue_assignee_id)

            if assignee_user not in issue.project.contributors.all():
                raise PermissionDenied("Assignee User must be contributor of the project")
            issue.issue_assignee = assignee_user

        # Enable partial updation of fields
        partial = True
        serializer = self.get_serializer(issue, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        try:
            issue = self.get_object()
        except Issues.DoesNotExist:
            return Response({'message': "Issue does not exist in this project"},
                            status=status.HTTP_404_NOT_FOUND)

        # Explicitly check object permission for DELETE method
        self.check_object_permissions(request, issue)
        super().destroy(request, *args, **kwargs)
        return Response({
            'Message': 'Issue has been deleted successfully'
        }, status=status.HTTP_200_OK)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [CommentAuthentication]
    queryset = Comments.objects.all()
    lookup_field = 'id'


    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        issue_id = self.kwargs.get('issue_id')

        if not Projects.objects.filter(id=project_id).exists():
            raise NotFound("Project does not exist")

        if not Issues.objects.filter(id=issue_id, project=project_id).exists():
            raise NotFound("Issue does not exist in this project")

        # Check if logged-in user is contributor of the project
        project = Projects.objects.get(id=project_id)
        if self.request.user not in project.contributors.all():
            raise PermissionDenied("You are not a contributor of this project")

        return self.queryset.filter(issue=issue_id)

    def perform_create(self, serializer):
        issue_id = self.kwargs.get('issue_id')
        serializer.save(comment_author=self.request.user, issue=issue_id)

    def update(self, request, *args, **kwargs):
        try:
            comment_obj = self.get_object()
        except Comments.DoesNotExist:
            return Response({'message': "Comment does not exist in this issue"},
                            status=status.HTTP_404_NOT_FOUND)

        # Explicitly check object permission for PUT method
        self.check_object_permissions(request, comment_obj)

        # Enable partial updation of fields
        partial = True
        serializer = self.get_serializer(comment_obj, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        try:
            comment_obj = self.get_object()
        except Comments.DoesNotExist:
            return Response({'message': "Comment does not exist in this issue"},
                            status=status.HTTP_404_NOT_FOUND)

        # Explicitly check object permission for DELETE method
        self.check_object_permissions(request, comment_obj)
        super().destroy(request, *args, **kwargs)
        return Response({
            'Message': 'Comment has been deleted successfully'
        }, status=status.HTTP_200_OK)
