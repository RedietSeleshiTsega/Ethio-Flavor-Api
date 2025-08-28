from django.db import models
from django.contrib.auth.models import User  

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)  

    def __str__(self):
        return self.name

class CulturalTag(models.Model):
    name = models.CharField(max_length=100, unique=True)  

    def __str__(self):
        return self.name

class Recipe(models.Model):
    DIFFICULTY_LEVELS = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Expert', 'Expert'),
    ]

    title = models.CharField(max_length=200)
    instructions = models.TextField() 
    prep_time = models.PositiveIntegerField()  
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS, default='Beginner')
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True) 

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    ingredients = models.ManyToManyField(Ingredient)
    cultural_tags = models.ManyToManyField(CulturalTag, blank=True)

    def __str__(self):
        return self.title