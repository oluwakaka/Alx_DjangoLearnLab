from rest_framework import serializers
from .models import Author, Book
import datetime


class BookSerializer(serializers.ModelSerializer):
    """
    Serializes all fields of the Book model.
    Includes validation to ensure publication year is not in the future.
    """

    class Meta:
        model = Book
        fields = "__all__"

    def validate_publication_year(self, value):
        current_year = datetime.date.today().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializes Author data along with nested books.
    Demonstrates handling of one-to-many relationship between Author and Book.
    """
    books = BookSerializer(many=True, read_only=True)  # Nested serializer

    class Meta:
        model = Author
        fields = ["id", "name", "books"]
