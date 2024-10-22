from django.contrib import admin
from .models import Projects, Contributors, Issues, Comments

# Register your models here
admin.site.register(Projects)
admin.site.register(Contributors)
admin.site.register(Issues)
admin.site.register(Comments)