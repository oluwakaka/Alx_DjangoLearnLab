from django.contrib.auth.decorators import user_passes_test, login_required
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .models import Library, Book
from django.views.generic.detail import DetailView
from django.contrib import messages

# Helper functions for role checks
def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == UserProfile.ROLE_ADMIN

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == UserProfile.ROLE_LIBRARIAN

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == UserProfile.ROLE_MEMBER

# Admin view
@user_passes_test(is_admin)
@login_required
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

# Librarian view
@user_passes_test(is_librarian)
@login_required
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

# Member view
@user_passes_test(is_member)
@login_required
def member_view(request):
    return render(request, 'relationship_app/member_view.html')


# Function-based view
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html" 
    context_object_name = 'library'



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'relationship_app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return render(request, 'relationship_app/logout.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # This triggers our signal to create UserProfile
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('login')  # redirect to login page
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

