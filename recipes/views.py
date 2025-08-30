from rest_framework import generics, permissions, viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Recipe, Category, Ingredient, CulturalTag, Review, Favorite
from .serializers import (
    RecipeSerializer, CategorySerializer,
    IngredientSerializer, CulturalTagSerializer, ReviewSerializer
)

# Custom permission: only owners can modify, others read-only
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'cultural_tags', 'difficulty', 'user']
    search_fields = ['title', 'description', 'ingredients__name', 'cultural_tags__name']
    ordering_fields = ['created_at', 'updated_at', 'prep_time', 'cook_time']
    ordering = ['-created_at']

    def get_queryset(self):
        # Base: only public recipes
        queryset = super().get_queryset().filter(is_public=True)

        # If authenticated, include user's private recipes
        if self.request.user.is_authenticated:
            private = Recipe.objects.filter(user=self.request.user, is_public=False)
            queryset = queryset | private

        return queryset.distinct()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # ---- Extra actions ----
    @action(detail=True, methods=['post'])
    def favorite(self, request, pk=None):
        recipe = self.get_object()
        favorite, created = Favorite.objects.get_or_create(user=request.user, recipe=recipe)

        if not created:
            favorite.delete()
            return Response({'status': 'removed from favorites'})
        return Response({'status': 'added to favorites'})

    @action(detail=True, methods=['post'])
    def review(self, request, pk=None):
        recipe = self.get_object()
        serializer = ReviewSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def my_recipes(self, request):
        recipes = Recipe.objects.filter(user=request.user)
        page = self.paginate_queryset(recipes)
        if page is not None:
            return self.get_paginated_response(self.get_serializer(page, many=True).data)
        return Response(self.get_serializer(recipes, many=True).data)

    @action(detail=False, methods=['get'])
    def my_favorites(self, request):
        favorites = Recipe.objects.filter(favorited_by__user=request.user)
        page = self.paginate_queryset(favorites)
        if page is not None:
            return self.get_paginated_response(self.get_serializer(page, many=True).data)
        return Response(self.get_serializer(favorites, many=True).data)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        return super().get_queryset().filter(recipe__is_public=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ---- Simple List Views ----
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class IngredientListView(generics.ListAPIView):
    queryset = Ingredient.objects.all().order_by('name')
    serializer_class = IngredientSerializer
    permission_classes = [permissions.AllowAny]


class CulturalTagListView(generics.ListAPIView):
    queryset = CulturalTag.objects.all().order_by('name')
    serializer_class = CulturalTagSerializer
    permission_classes = [permissions.AllowAny]
