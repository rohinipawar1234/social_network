from django.contrib import admin
from social.models import CustomUser,FriendRequest

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(FriendRequest)

