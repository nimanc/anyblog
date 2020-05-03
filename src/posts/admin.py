from django.contrib import admin
from .models import Author, Post, Category


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)