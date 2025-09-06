# Social Media API (Django + DRF)

## Features
- Custom `User` model extending `AbstractUser` with `bio`, `profile_picture`, and self-referential `followers` (symmetrical=False)
- Token authentication (`rest_framework.authtoken`)
- Endpoints:
  - `POST /api/accounts/register` – create user and return token
  - `POST /api/accounts/login` – login with **username or email** and return token
  - `GET/PUT /api/accounts/profile` – retrieve/update own profile (token required)

## Setup
```bash
python -m venv .venv
source .venv/Scripts/activate   # Windows Git Bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
