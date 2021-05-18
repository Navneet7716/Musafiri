from django.contrib import admin
from .models import Destination , blog_user , Flight , Train , Hotel , History_Flight , History_Train , History_Package , History_Hotel
# Register your models here.

admin.site.register(Destination)

admin.site.register(blog_user)

admin.site.register(Flight)

admin.site.register(Train)

admin.site.register(Hotel)

admin.site.register(History_Flight)

admin.site.register(History_Package)

admin.site.register(History_Train)

admin.site.register(History_Hotel)