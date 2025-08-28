# recipes/views.py
from rest_framework import generics, permissions
from .models import Recipe
from .serializers import RecipeSerializer

class RecipeListCreateView(generics.ListCreateAPIView):
    queryset = Recipe.objects.all().order_by('-created_at')
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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