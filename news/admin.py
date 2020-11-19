from django.contrib import admin
from .models import FlashUser, Article, CategoryString, NewspaperString

admin.site.register(FlashUser)
admin.site.register(Article)
admin.site.register(CategoryString)
admin.site.register(NewspaperString)
