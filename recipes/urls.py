from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecipeViewSet, ReviewViewSet, CategoryListView, IngredientListView, CulturalTagListView

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet, basename="recipe")
router.register(r'reviews', ReviewViewSet, basename="review")

urlpatterns = [
    path('', include(router.urls)),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('ingredients/', IngredientListView.as_view(), name='ingredient-list'),
    path('cultural-tags/', CulturalTagListView.as_view(), name='cultural-tag-list'),
]
