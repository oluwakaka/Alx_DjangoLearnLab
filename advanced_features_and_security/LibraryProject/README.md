# Django Permissions & Groups Setup

This project demonstrates custom user permissions and groups.

## Permissions
Defined in `bookshelf/models.py` under the `Book` model:
- `can_create` → Create new books
- `can_edit` → Edit books
- `can_delete` → Delete books
- `can_view` → View books

## Groups
Defined in `bookshelf/permissions_setup.py`:
- **Editors** → can_create, can_edit
- **Viewers** → can_view
- **Admins** → all permissions

## Views
Protected using `@permission_required` decorators in `bookshelf/views.py`.

## How to Test
1. Create users and assign them to groups in Django Admin.
2. Try accessing `/create_book`, `/edit_book`, `/delete_book`, `/view_book`.
3. Only users with the right group permissions will succeed.
