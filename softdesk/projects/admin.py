from django.contrib import admin
from .models import Projects, Contributors, Issues

# Register your models here
admin.site.register(Projects)
admin.site.register(Contributors)
admin.site.register(Issues)