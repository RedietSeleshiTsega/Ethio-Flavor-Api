from rest_framework import serializers
from .models import Recipe, Category, Ingredient, CulturalTag, Review, Favorite, RecipeIngredient

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

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['user', 'created_at']

class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient_name = serializers.CharField(source='ingredient.name', read_only=True)
    
    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'ingredient_name', 'quantity', 'unit']

class RecipeSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(many=True, read_only=True, source='recipeingredient_set')
    cultural_tags = CulturalTagSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    user = serializers.StringRelatedField(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True, required=False
    )
    ingredient_data = serializers.JSONField(write_only=True, required=False)
    cultural_tag_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=CulturalTag.objects.all(), source='cultural_tags', write_only=True, required=False
    )

    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'instructions', 'prep_time', 'cook_time', 
            'servings', 'difficulty', 'image', 'created_at', 'updated_at', 'is_public',
            'user', 'category', 'ingredients', 'cultural_tags', 'reviews', 'average_rating', 'is_favorited',
            'category_id', 'ingredient_data', 'cultural_tag_ids'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']

    def get_average_rating(self, obj):
        return obj.average_rating()

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.favorited_by.filter(user=user).exists()
        return False

    def create(self, validated_data):
        ingredient_data = validated_data.pop('ingredient_data', [])
        cultural_tags = validated_data.pop('cultural_tags', [])
        
        recipe = Recipe.objects.create(**validated_data)
        
        # Add cultural tags
        recipe.cultural_tags.set(cultural_tags)
        
        # Add ingredients with quantities
        for item in ingredient_data:
            ingredient = Ingredient.objects.get(id=item['ingredient_id'])
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                quantity=item.get('quantity', ''),
                unit=item.get('unit', '')
            )
        
        return recipe

    def update(self, instance, validated_data):
        ingredient_data = validated_data.pop('ingredient_data', None)
        cultural_tags = validated_data.pop('cultural_tags', None)
        
        # Update basic fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update cultural tags if provided
        if cultural_tags is not None:
            instance.cultural_tags.set(cultural_tags)
        
        # Update ingredients if provided
        if ingredient_data is not None:
            # Clear existing ingredients
            instance.recipeingredient_set.all().delete()
            
            # Add new ingredients
            for item in ingredient_data:
                ingredient = Ingredient.objects.get(id=item['ingredient_id'])
                RecipeIngredient.objects.create(
                    recipe=instance,
                    ingredient=ingredient,
                    quantity=item.get('quantity', ''),
                    unit=item.get('unit', '')
                )
        
        return instance