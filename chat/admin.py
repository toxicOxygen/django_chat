from django.contrib import admin
from .models import Message, MessageHead

# Register your models here.
admin.site.register(Message)
admin.site.register(MessageHead)