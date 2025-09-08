# api/views.py
from rest_framework import generics, viewsets
from .models import Book
from .serializers import BookSerializer

# Existing simple list view
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# New ViewSet for full CRUD
class BookViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for Book model:
    - list, retrieve, create, update, partial_update, destroy
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
