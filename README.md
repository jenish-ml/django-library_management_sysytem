# Library Management System

A simple Django-based Library Management System with three user roles (Admin, Librarian, Member). It allows members to borrow and return books, librarians to manage the book catalog, and admins to oversee users and roles.

---

## Features

- **User Authentication** – Register, login, logout.
- **Role‑based Access** – Admin, Librarian, Member.
- **Book Management** – Add, edit, delete, search, and filter books.
- **Member Management** – View and edit profile, see borrowed books.
- **Borrow/Return System** – Issue books, track due dates, update available copies automatically.
- **Admin Panel** – Full control over users, roles, categories, and books.

---

## Tech Stack

- **Backend**: Django 4.x (Python 3.8+)
- **Database**: PostgreSQL
- **Frontend**: HTML, Bootstrap 5 (templates)
- **Other**: Django’s built‑in authentication, class‑based & function‑based views

---

## Prerequisites

- Python 3.8 or higher
- PostgreSQL (installed and running)
- Git (optional, for cloning)

---

## Installation

### 1. Clone the repository

bash
git clone https://github.com/yourusername/library-management-system.git
cd library-management-system

### 2. Create and activate a virtual environment

python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

### 3. Install dependencies

pip install django psycopg2-binary

### 4. Set up PostgreSQL
Create a database and user:

CREATE DATABASE library_db;
CREATE USER library_user WITH PASSWORD 'your_password';
ALTER ROLE library_user SET client_encoding TO 'utf8';
ALTER ROLE library_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE library_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE library_db TO library_user;

### 5. Configure database settings
Edit library_project/settings.py and update the DATABASES section with your PostgreSQL credentials.

### 6. Apply migrations

python manage.py makemigrations accounts books
python manage.py migrate

### 7. Create a superuser (admin)

python manage.py createsuperuser

### 8. Run the development server

python manage.py runserver
Visit http://127.0.0.1:8000/ to see the application.
