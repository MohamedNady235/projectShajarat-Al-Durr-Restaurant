# Shajarat Al-Durr Restaurant

## Project Overview

Shajarat Al-Durr Restaurant is a modern Django-based restaurant website designed to showcase a premium dining experience, feature menu items, allow online orders, manage reservations, and collect visitor inquiries. The project combines a clean Arabic-inspired visual style with responsive layouts to provide a smooth user experience across desktop and mobile devices.

## Features

- Modern restaurant website
- Arabic RTL interface
- Restaurant menu
- Food details
- Online order form
- Table reservation
- Contact form
- Responsive design
- User-friendly interface

## Technologies Used

- Python
- Django
- HTML5
- CSS3
- JavaScript
- SQLite / Database used by the project
- Git & GitHub

## Pages

- Home
- Menu
- Order
- Reservation
- Contact
- Gallery / About if available

## Project Structure

```text
project/
├── cafeteria/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── migrations/
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── cafeteria_project/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── media/
│   ├── README.txt
│   ├── gallery_images/
│   └── menu_images/
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── script.js
├── templates/
│   ├── about.html
│   ├── base.html
│   ├── contact.html
│   ├── footer.html
│   ├── gallery.html
│   ├── home.html
│   ├── menu_detail.html
│   ├── menu_list.html
│   ├── navbar.html
│   ├── order_confirmation.html
│   ├── place_order.html
│   └── reserve_table.html
├── .env.example
├── .gitignore
├── db.sqlite3
├── manage.py
├── README.md
├── requirements.txt
└── Project.zip
```

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Shajarat-Al-Durr-Restaurant
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate      # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment variables:
   ```bash
   copy .env.example .env
   ```
   Then update the values inside `.env` as needed.
5. Apply database migrations:
   ```bash
   python manage.py migrate
   ```
6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Virtual Environment

To create a virtual environment in the project folder:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Activate it on macOS/Linux:

```bash
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Database

The project uses SQLite by default, which is configured in the Django settings file. To initialize the database:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Run the Project

```bash
python manage.py runserver
```

## Screenshots

The project includes restaurant website pages such as the home page, menu, reservation, and contact sections. Add screenshots here after local testing:

- home-page.png
- menu-page.png
- reservation-page.png
- contact-page.png

## Future Improvements

- Add user authentication for admin and staff roles
- Add online payment integration
- Improve menu search and filtering
- Add an admin dashboard for orders and reservations
- Expand the gallery and blog sections
- Support multilingual content management

## Author

Mohamed Nady
