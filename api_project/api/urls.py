# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # Old list view (optional)
    path('books/', BookList.as_view(), name='book-list'),

    # Include router URLs for CRUD operations
    path('', include(router.urls)),
]
