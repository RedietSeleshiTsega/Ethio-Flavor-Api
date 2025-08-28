from django.contrib import admin
from .models import Category, Ingredient, CulturalTag, Recipe

admin.site.register(Category)
admin.site.register(Ingredient)
admin.site.register(CulturalTag)
admin.site.register(Recipe)