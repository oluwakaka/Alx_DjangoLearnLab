# Social Media API (Django + DRF Token Auth)

## Stack
- Django (custom user model)
- Django REST Framework
- DRF Token Authentication

## Quickstart

```bash
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver


## Follow / Feed endpoints

- `POST /api/auth/follow/<user_id>/` — follow a user (auth required)
- `POST /api/auth/unfollow/<user_id>/` — unfollow a user (auth required)
- `GET /api/auth/following/` — list users you follow (auth required)
- `GET /api/auth/followers/` — list users who follow you (auth required)
- `GET /api/feed/` — list posts from users you follow, ordered by created_at desc (auth required)

Examples:
curl -H "Authorization: Token <token>" http://127.0.0.1:8000/api/feed/
