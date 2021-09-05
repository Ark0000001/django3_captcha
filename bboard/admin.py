from django.contrib import admin

from .models import Bb
from .models import Rubric
from django.db.models import Q




admin.site.register(Rubric)

class BbAdmin(admin.ModelAdmin):
    list_display = ('title', 'rubric', 'content', 'price', 'published')
    list_display_links=('title','content', 'rubric',)

    search_fields = ('title', 'content',)




admin.site.register(Bb, BbAdmin)
