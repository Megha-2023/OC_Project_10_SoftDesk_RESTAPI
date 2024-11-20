from rest_framework import serializers
from django.core.exceptions import PermissionDenied
from authentication.models import Users
from .models import Projects, Contributors, Issues, Comments
from authentication.serializers import UserSerializer


class ContributorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contributors
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    contributors = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    
    def get_contributors(self, instance):
        queryset = instance.contributors.all()
        serializer = UserSerializer(queryset, many=True)
        return serializer.data
    
    def get_author(self, instance):
        queryset = instance.author
        serializer = UserSerializer(queryset)
        return serializer.data

    def validate(self, attrs):
        attrs["author"] = self.context["request"].user
        return attrs
    
    def create(self, validated_data):
        contributors = validated_data.pop("contributors", [])
        # validated_data['author'] = self.current_user
        project_obj = Projects.objects.create(**validated_data)
        project_obj.contributors.add(project_obj.author_id,
                                     through_defaults={'role': 'Author'})
        # Contributors.objects.create(project_id=project_obj.id, user_id=project_obj.author_id, role="Author")
        for contributor in contributors:
            project_obj.contributors.add(contributor.id)

        return project_obj
    
    class Meta:
        model = Projects
        fields = ['id', 'title', 'description', 'author', 'contributors', 'type']
        read_only_fields = ['author']


class IssueSerializer(serializers.ModelSerializer):
    issue_author = serializers.SerializerMethodField()
    issue_assignee = serializers.SerializerMethodField()
    project_id = serializers.SerializerMethodField()

    def get_issue_author(self, instance):
        queryset = instance.issue_author
        serializer = UserSerializer(queryset)
        return serializer.data
    
    def get_issue_assignee(self, instance):
        queryset = instance.issue_assignee
        serializer = UserSerializer(queryset)
        return serializer.data
    
    def get_project_id(self, instance):
        queryset = instance.project
        serializer = ProjectSerializer(queryset)
        return serializer.data['id']
    
    """def validate(self, attrs):
        attrs["issue_author"] = self.context["request"].user
        return attrs"""
    

    def create(self, validated_data):
        project_id = self.context.get('view').kwargs.get('project_id')
        project_obj = Projects.objects.get(id=project_id)
        validated_data['project'] = project_obj
        data_passed = self.context['request'].data
        # check if the assignee user is in contributors list or not
        issue_assignee_id = data_passed.get('issue_assignee')
        if issue_assignee_id:
            assignee_user = Users.objects.get(id=issue_assignee_id)
            
            if assignee_user not in project_obj.contributors.all():
                raise PermissionDenied("Assignee User must be contributor of the project")
            validated_data['issue_assignee'] = assignee_user    
        else:
            validated_data['issue_assignee'] = validated_data['issue_author']

        issue_obj = Issues.objects.create(**validated_data)
        return issue_obj

    class Meta:
        model = Issues
        fields = ['id', 'title', 'description', 'priority', 'status', 'tag', 'created_time', 'project_id', 'issue_author', 'issue_assignee']