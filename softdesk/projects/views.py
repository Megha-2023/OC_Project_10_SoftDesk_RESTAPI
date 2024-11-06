from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from authentication.serializers import UserSerializer
from .models import Projects, Contributors
from .serializers import ProjectSerializer, ContributorSerializer
from .permissions import ProjectAuthentication


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, ProjectAuthentication]
    queryset = Projects.objects.all()
    lookup_field = 'id'

    def retrieve(self, request, id=None):
        queryset = Projects.objects.filter(author=request.user, id=id)
        if not queryset:
            return Response({'Error': 'You do not have access to the project'},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = ProjectSerializer(queryset, many=True)
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )
    
    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({
            'Message': 'Project has been deleted successfully'
        }, status=status.HTTP_200_OK)

    """@action(detail=False, methods=["GET"])  #try to set detail=false
    def users(self, request, id=None):
        project = self.get_object()
        contributors = project.contributors  # Contributors.objects.filter(project=project)
        serializer = UserSerializer(contributors, many=True)
        return Response({
                'contributors': serializer.data
            }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def users(self, request, id=None):
        # check for user exists, then update either using email or username
        project = self.get_object()
        users_data = request.data
        users_data['project'] = project.id
        
        serializer = ProjectSerializer(data=users_data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'User saved successfully'
            }, status=status.HTTP_200_OK)
        return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )"""


class ProjectContributorsAPIView(APIView):
    def get(self, request, id):
        project = Projects.objects.get(id=id)
        contributors = project.contributors.all()
        serializer = UserSerializer(contributors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

