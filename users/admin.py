from django.contrib import admin
from .models import Destination , blog_user , Flight , Train , Hotel
# Register your models here.

admin.site.register(Destination)

admin.site.register(blog_user)

admin.site.register(Flight)

admin.site.register(Train)

admin.site.register(Hotel)