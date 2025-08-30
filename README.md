# EthioFlavor API

A comprehensive RESTful API for managing Ethiopian recipes with user authentication, advanced filtering, and cultural tagging features.

## Overview

EthioFlavor is a Django REST Framework-based API that allows users to explore, create, and share authentic Ethiopian recipes. The application features user authentication, recipe management, review systems, favorites functionality, and cultural categorization.

## Features

- **User Authentication**: JWT-based authentication system with registration and login endpoints
- **Recipe Management**: Full CRUD operations for Ethiopian recipes with images
- **Categorization**: Organize recipes by categories, ingredients, and cultural tags
- **Review System**: Users can rate and comment on recipes
- **Favorites**: Bookmark favorite recipes for quick access
- **Advanced Filtering**: Search and filter recipes by various criteria
- **Pagination**: Efficient data retrieval with paginated responses
- **User Profiles**: Custom user profiles with culinary preferences

## Technology Stack

- **Backend Framework**: Django 5.2.5
- **API Framework**: Django REST Framework
- **Authentication**: JWT (Simple JWT)
- **Database**: SQLite (default, configurable for production)
- **File Storage**: Local filesystem (configurable for cloud storage)
- **Filtering**: Django Filter Backend

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ethioflavor_project
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## Environment Configuration

For production deployment, configure these environment variables:

- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DATABASE_URL`: Database connection string (for production databases)
- `SECRET_KEY`: Django secret key (change from default in production)

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/token/` - Obtain JWT tokens
- `POST /api/token/refresh/` - Refresh JWT tokens

### Recipes
- `GET /api/recipes/` - List all public recipes
- `POST /api/recipes/` - Create a new recipe (authenticated)
- `GET /api/recipes/{id}/` - Retrieve a specific recipe
- `PUT/PATCH /api/recipes/{id}/` - Update a recipe (owner only)
- `DELETE /api/recipes/{id}/` - Delete a recipe (owner only)
- `POST /api/recipes/{id}/favorite/` - Toggle favorite status
- `POST /api/recipes/{id}/review/` - Add a review
- `GET /api/recipes/my_recipes/` - Get user's recipes (authenticated)
- `GET /api/recipes/my_favorites/` - Get user's favorites (authenticated)

### Categories, Ingredients & Tags
- `GET /api/recipes/categories/` - List all categories
- `GET /api/recipes/ingredients/` - List all ingredients
- `GET /api/recipes/cultural-tags/` - List all cultural tags

### Users
- `GET /api/users/` - List users (admin only)
- `GET/PUT/PATCH /api/users/{id}/` - User details (self or admin)

## Data Models

### Recipe
- Title, description, instructions
- Preparation and cooking times
- Difficulty level (Beginner, Intermediate, Expert)
- Category, ingredients, cultural tags
- User ownership and privacy settings
- Image upload support

### User
- Extended Django User model with profile
- Bio, profile picture, culinary experience
- Dietary preferences and skill level

### Supporting Models
- Category: Recipe categories (e.g., Main Dish, Appetizer)
- Ingredient: Recipe ingredients with quantities
- Cultural Tag: Regional or cultural identifiers
- Review: User ratings and comments
- Favorite: User recipe bookmarks

## Authentication & Permissions

- **Public Access**: Read-only access to public recipes and lists
- **Authenticated Users**: Can create content, favorite recipes, and leave reviews
- **Ownership-Based**: Users can only modify their own content
- **Admin Access**: Full administrative privileges

## Filtering & Search

Recipes can be filtered by:
- Category
- Cultural tags
- Difficulty level
- User
- Search terms in title, description, ingredients, or tags

## Pagination

API responses are paginated with a default page size of 10 items, configurable via query parameters.

## File Uploads

Recipe images are stored in the `media/recipes/` directory with support for configurable cloud storage in production.

## Deployment Notes

1. Set `DEBUG = False` in production
2. Configure a production database (PostgreSQL recommended)
3. Set up proper static file serving
4. Configure media storage (consider cloud storage for production)
5. Set appropriate CORS headers if consuming from different domains
6. Use environment variables for sensitive configuration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## Support

For support or questions, please contact the development team or create an issue in the project repository.
