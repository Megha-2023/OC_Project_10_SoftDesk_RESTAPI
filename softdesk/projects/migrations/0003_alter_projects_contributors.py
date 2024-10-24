# Generated by Django 5.1.1 on 2024-10-22 07:12

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_rename_project_id_contributors_project_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='projects',
            name='contributors',
            field=models.ManyToManyField(blank=True, through='projects.Contributors', to=settings.AUTH_USER_MODEL),
        ),
    ]
