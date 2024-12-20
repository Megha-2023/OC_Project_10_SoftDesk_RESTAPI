from django.db import models
from authentication.models import Users


# Create your models here.
class Projects(models.Model):
    """ Project model class"""

    class TypeProject(models.TextChoices):
        BACK_END = 'Back_end'
        FRONT_END = 'Front_end'
        IOS = 'iOS'
        ANDROID = 'Android'

    title = models.CharField(max_length=120)
    description = models.TextField(max_length=500, blank=True)
    type = models.CharField(max_length=50, choices=TypeProject.choices, blank=True)
    author = models.ForeignKey(to=Users, on_delete=models.CASCADE, related_name='+')
    contributors = models.ManyToManyField(Users, through='Contributors', blank=True)


class Contributors(models.Model):
    """ Class working as a Junction table between Users and Projects"""
    user = models.ForeignKey(to=Users, on_delete=models.CASCADE, related_name='+')
    project = models.ForeignKey(to=Projects, on_delete=models.CASCADE, related_name='+')
    role = models.CharField(max_length=25, blank=True)

    class Meta:
        """ Meta class"""
        unique_together = ("user", "project")


class Issues(models.Model):
    class Priority(models.TextChoices):
        LOW = 'Low'
        MEDIUM = 'Medium'
        HIGH = 'High'

    class Tags(models.TextChoices):
        BUG = 'Bug'
        ENHANCEMENT = 'Enhancement'
        TASK = 'Task'

    class Status(models.TextChoices):
        TO_DO = 'To-Do'
        IN_PROGRESS = 'In_progress'
        COMPLETED = 'Completed'

    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500, blank=True)
    project = models.ForeignKey(to=Projects, on_delete=models.CASCADE, related_name='project_id')
    tag = models.CharField(max_length=50, choices=Tags.choices, default=Tags.TASK)
    priority = models.CharField(max_length=50, choices=Priority.choices, default=Priority.LOW)
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.TO_DO)
    issue_author = models.ForeignKey(to=Users, on_delete=models.CASCADE, related_name='issue_author')
    issue_assignee = models.ForeignKey(to=Users, on_delete=models.CASCADE, blank=True, related_name='issue_assignee')
    created_time = models.DateTimeField(auto_now_add=True)


class Comments(models.Model):
    description = models.TextField(max_length=500, blank=True)
    comment_author = models.ForeignKey(to=Users, on_delete=models.CASCADE, related_name='+')
    issue = models.ForeignKey(to=Issues, on_delete=models.CASCADE, related_name='issue_id')
    created_time = models.DateTimeField(auto_now_add=True)
