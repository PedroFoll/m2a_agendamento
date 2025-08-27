from django.contrib import admin
from django.utils.html import format_html

from core.models import ImageModel

class DemoModelCustomAdmin(admin.ModelAdmin):
    list_display=("title", "image1")

    def image1(self,obj):
        return format_html('<img srt="{0}"width="auto" hight="150px">'.format(obj.image.url))

admin.site.register(ImageModel,DemoModelCustomAdmin)

