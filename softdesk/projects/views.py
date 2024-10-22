from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Projects
from .serializers import ProjectSerializer
from .permissions import ProjectAuthentication


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, ProjectAuthentication]

    def retrieve(self, request, pk=None):
        queryset = Projects.objects.filter(author=request.user, id=pk)

        if not queryset:
            return Response({'Error': 'You do not have access to the project'},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = ProjectSerializer(queryset, many=True)
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )
    
    def get_queryset(self):
        return Projects.objects.filter(author=self.request.user)

    



