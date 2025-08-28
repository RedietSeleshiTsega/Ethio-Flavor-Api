from rest_framework import generics, permissions
from .models import Recipe
from .serializers import RecipeSerializer, CategorySerializer, IngredientSerializer, CulturalTagSerializer
from .models import Category, Ingredient, CulturalTag
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class RecipeListCreateView(generics.ListCreateAPIView):
    queryset = Recipe.objects.all().order_by('-created_at')
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'cultural_tags']
    search_fields = ['title', 'ingredients__name']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if self.request.method in permissions.SAFE_METHODS:
                return Recipe.objects.all()
            return Recipe.objects.filter(user=user)
        return Recipe.objects.all()
    
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer

class IngredientListView(generics.ListAPIView):
    queryset = Ingredient.objects.all().order_by('name')
    serializer_class = IngredientSerializer

class CulturalTagListView(generics.ListAPIView):
    queryset = CulturalTag.objects.all().order_by('name')
    serializer_class = CulturalTagSerializer 