from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Book

def run():
    content_type = ContentType.objects.get_for_model(Book)

    # Get permissions
    can_create = Permission.objects.get(codename="can_create", content_type=content_type)
    can_edit = Permission.objects.get(codename="can_edit", content_type=content_type)
    can_delete = Permission.objects.get(codename="can_delete", content_type=content_type)
    can_view = Permission.objects.get(codename="can_view", content_type=content_type)

    # Create groups
    editors, _ = Group.objects.get_or_create(name="Editors")
    viewers, _ = Group.objects.get_or_create(name="Viewers")
    admins, _ = Group.objects.get_or_create(name="Admins")

    # Assign permissions
    editors.permissions.set([can_create, can_edit])
    viewers.permissions.set([can_view])
    admins.permissions.set([can_create, can_edit, can_delete, can_view])

    print("Groups and permissions successfully created.")
