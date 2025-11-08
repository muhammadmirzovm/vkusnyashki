🍔 Vkusnyashki - Fast Food Menu

Vkusnyashki is a real-time fast food menu web application.
The frontend is built with HTML, Tailwind CSS, and JavaScript, while the backend uses Django + ASGI (Daphne) for real-time updates.

📌 Features

Fast food menu cards: Burger, pizza, fries, and more.

Real-time CRUD operations: Create, edit, delete menu items instantly.

Availability filter: Only shows items marked as available (is_available).

Responsive design: Works seamlessly on desktop, tablet, and mobile devices.

Image support: Upload and display food images with Django ImageField.

Real-time updates: Powered by Server-Sent Events (SSE).

Admin panel: Full menu management via Django admin.

⚙️ Technologies

Backend: Django 5.2.x

ASGI Server: Daphne

Frontend: HTML, Tailwind CSS, JavaScript

Database: SQLite (default, compatible with other databases)

Images: Pillow

Package manager / virtual environment: UV

🛠️ Installation

Clone the repository:

git clone https://github.com/muhammadmirzovm/vkusnyashki
cd vkusnyashki


Set up a virtual environment with UV:

uv venv .venv
uv venv activate .venv


Install dependencies:

uv install -r requirements.txt


Apply database migrations:

uv run python manage.py makemigrations
uv run python manage.py migrate


Run the development server:

uv run python manage.py runserver

📂 Project Structure (Optional)

backend/ — Django backend

frontend/ — HTML, CSS, JavaScript files

media/ — Uploaded images

requirements.txt — Python dependencies

Notes

Ensure Python 3.11+ is installed.

Supports real-time updates using SSE.

Admin panel accessible at /admin for managing menu items.