from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Book, Library

# Function-based view
from django.http import HttpResponse
from .models import Book

def list_books(request):
    books = Book.objects.all()
    book_list = "\n".join([f"{book.title} by {book.author.name}" for book in books])
    return HttpResponse(book_list, content_type="text/plain")


# Class-based view
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'
