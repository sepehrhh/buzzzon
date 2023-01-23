from django.contrib import admin

from .models import *

admin.site.register(Room)
admin.site.register(Contact)
admin.site.register(Group)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'type')
