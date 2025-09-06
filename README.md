# Django E-Commerce Store

A modern e-commerce web application built with Django 5, Python 3.12, Bootstrap 5, and Stripe for payments.

## Features
- Product catalog and detail pages
- Shopping cart with session support
- User registration and login
- Stripe payment integration
- Mobile-friendly responsive design
- Custom admin theming with Jazzmin
- Dark mode toggle

## Getting Started

### 1. Clone the Repository
```
git clone https://github.com/RedHoodJT1988/django_ecommerce.git
cd django_ecommerce
```

### 2. Create and Activate a Virtual Environment
```
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```
pip install -r requirements.txt
```
If `requirements.txt` is missing, install manually:
```
pip install django==5.* stripe python-dotenv jazzmin
```

### 4. Set Up Environment Variables
Create a `.env` file in the project root:
```
STRIPE_PUBLIC_KEY=your_stripe_public_key
STRIPE_SECRET_KEY=your_stripe_secret_key
```

### 5. Apply Migrations
```
python manage.py migrate
```

### 6. Create a Superuser (for admin access)
```
python manage.py createsuperuser
```

### 7. Collect Static Files (optional, for production)
```
python manage.py collectstatic
```

### 8. Run the Development Server
```
python manage.py runserver
```
Visit [http://localhost:8000](http://localhost:8000) in your browser.

## Stripe Testing
- Use Stripe test keys in your `.env` file.
- Test card: `4242 4242 4242 4242` (any future date, any CVC)

## Admin Panel
- Visit `/admin/` and log in with your superuser credentials.
- Admin is themed with Jazzmin and supports dark mode.

## Customization
- Logo and color palette can be changed in `core/settings.py` and static files.
- Modify templates in `store/templates/store/` for UI changes.

## License
MIT License

---
For any issues, open an issue on the repository or contact the maintainer.
