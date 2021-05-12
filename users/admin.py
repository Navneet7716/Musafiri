from django.contrib import admin
from .models import Destination , blog_user , Flight
# Register your models here.

admin.site.register(Destination)

admin.site.register(blog_user)

admin.site.register(Flight)