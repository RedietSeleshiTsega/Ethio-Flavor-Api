from django.urls import path
from . import views

urlpatterns = [
    path('', views.RecipeListCreateView.as_view(), name='recipe-list-create'),
    path('<int:pk>/', views.RecipeDetailView.as_view(), name='recipe-detail'),
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('ingredients/', views.IngredientListView.as_view(), name='ingredient-list'),
    path('cultural-tags/', views.CulturalTagListView.as_view(), name='cultural-tag-list'),

]