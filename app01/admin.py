from django.contrib import admin
from app01 import models

# Register your models here.
admin.site.register(models.UserProfile)
admin.site.register(models.EmailCode)
admin.site.register(models.Tags)
admin.site.register(models.Category)
admin.site.register(models.Topic)
admin.site.register(models.Weibo)
admin.site.register(models.Comment)