from django.contrib import admin

from .models import Address, Feedback, Media, Restaurant

# Register your models here.


admin.site.register(Restaurant)
admin.site.register(Address)
admin.site.register(Media)
admin.site.register(Feedback)