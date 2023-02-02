from django.contrib import admin
from .models import Post, Comments
# Register your models here.
# admin.site.register((Post, Comments))
admin.site.register((Comments))

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    class Media:
        js = ('enjectscript.js',)
