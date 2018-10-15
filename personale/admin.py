from django.contrib import admin

from .models import Lavoratore

class LavoratoreAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'question_text']

admin.site.register(Lavoratore)
