from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(user)
admin.site.register(origin_resvation)
admin.site.register(approved_reservation)
admin.site.register(device)
admin.site.register(time_sep)
