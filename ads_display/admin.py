from django.contrib import admin
from .models import humans
# Register your models here.
@admin.register(humans)

class registerhumans(admin.ModelAdmin):
    list_display=["id","Date","Time","Total_Females","Total_Males","Total_attracted_humans",
                  "Total_present_humans"]