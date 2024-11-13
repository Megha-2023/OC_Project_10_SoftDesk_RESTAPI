from rest_framework import serializers
from .models import Projects, Contributors
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
    
    """def update(self, instance, validated_data):
        contributors = validated_data.pop('contributors')
        instance.author = validated_data.get('author', instance.author)
        instance.save()
        super().update(instance, validated_data)
        return instance
    """
    class Meta:
        model = Projects
        fields = ['id', 'title', 'description', 'author', 'contributors', 'type']
        read_only_fields = ['author']
