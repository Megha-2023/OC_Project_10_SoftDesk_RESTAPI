# Generated by Django 5.1.1 on 2024-11-05 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_alter_projects_contributors'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contributors',
            name='permission',
        ),
        migrations.AlterField(
            model_name='contributors',
            name='role',
            field=models.CharField(blank=True, max_length=25),
        ),
        migrations.AlterField(
            model_name='projects',
            name='type',
            field=models.CharField(blank=True, choices=[('Back_end', 'Back End'), ('Front_end', 'Front End'), ('iOS', 'Ios'), ('Android', 'Android')], max_length=50),
        ),
    ]
