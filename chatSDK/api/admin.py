from django.contrib import admin
from .models import *

# Register your models here.
admin.site.site_header = 'ChatSDK'
admin.site.register(Company)
admin.site.register(Query)

