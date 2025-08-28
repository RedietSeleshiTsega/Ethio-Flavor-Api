from rest_framework import serializers
from .models import Recipe, Category, Ingredient, CulturalTag

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']

class CulturalTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = CulturalTag
        fields = ['id', 'name']

class RecipeSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
    cultural_tags = CulturalTagSerializer(many=True, read_only=True)
    
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True, required=False
    )
    ingredient_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Ingredient.objects.all(), source='ingredients', write_only=True
    )
    cultural_tag_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=CulturalTag.objects.all(), source='cultural_tags', write_only=True, required=False
    )

    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'instructions', 'prep_time', 'difficulty',
            'category', 'ingredients', 'cultural_tags', 
            'category_id', 'ingredient_ids', 'cultural_tag_ids', 
            'created_at', 'updated_at'
        ]
 
        extra_kwargs = {
            'category': {'required': False},
            'cultural_tags': {'required': False},
        }