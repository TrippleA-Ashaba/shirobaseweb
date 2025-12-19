# Shirobase

![CI/CD](https://img.shields.io/badge/CI%2FCD-ready-blue?style=flat-square)
![Docker](https://img.shields.io/badge/docker-ready-blue?style=flat-square&logo=docker)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen?style=flat-square)
![Python](https://img.shields.io/badge/python-3.14+-blue?style=flat-square&logo=python)
![Django](https://img.shields.io/badge/django-5.2-green?style=flat-square&logo=django)

A production-ready Django skeleton project that serves as a solid starting point for building modern web applications with Django views and templates.

## 🎯 Overview

Shirobase is a production-ready Django skeleton project designed to jumpstart your development process. Instead of spending hours setting up the same boilerplate configurations for every new project, use Shirobase as your foundation.

**What's Included:**

-   Complete authentication system with Django views and templates
-   Two pre-built Django apps (users and accounts)
-   Template-based user interface with modern styling
-   Docker containerization
-   Testing framework with pytest
-   Code quality tools (Ruff linter)
-   Comprehensive middleware and security configurations
-   Development tools (debug toolbar, auto-reload)
-   Production-ready settings (WhiteNoise, logging, PostgreSQL support)
-   Optional REST API support (can be enabled if needed)

This skeleton comes with 20+ essential packages and best practices already integrated, allowing you to focus on building your application's unique features from day one.

## 🚀 Tech Stack

-   **Python 3.14** - Latest Python version
-   **Django 5.2** - Modern Django framework
-   **uv** - Fast Python package manager
-   **Django Templates** - Server-side rendering
-   **PostgreSQL/SQLite** - Database support
-   **Docker** - Containerization support
-   **Django REST Framework** - Optional REST API support (included but not primary)

## ✨ Features

This skeleton project includes:

### Core Setup

-   ✅ Pre-configured Django 5.2 setup
-   ✅ Modern Python 3.14 support
-   ✅ UV package management for lightning-fast dependency resolution
-   ✅ Docker configuration for containerized deployment
-   ✅ Clean project structure with organized apps

### Authentication & Authorization

-   ✅ Custom User model with Profile support
-   ✅ Django Allauth integration for complete authentication flows
-   ✅ Template-based login, registration, and password reset views
-   ✅ Session-based authentication
-   ✅ Custom permissions system (Smartmin)
-   ✅ Django Author for automatic created_by/modified_by tracking
-   ✅ Optional JWT authentication support (via REST API if needed)

### Web Development

-   ✅ Django views and templates configured
-   ✅ Modern, responsive UI templates
-   ✅ Form handling with Django forms
-   ✅ Custom CSRF middleware with configurable exemptions
-   ✅ Message framework for user notifications
-   ✅ Optional REST API support (Django REST Framework included)

### Database & Models

-   ✅ PostgreSQL support (with psycopg)
-   ✅ SQLite support for development
-   ✅ Django Extensions with TimeStampedModel
-   ✅ Phone number field support
-   ✅ Audit logging with django-auditlog

### Testing & Code Quality

-   ✅ Pytest configuration with Django integration
-   ✅ pytest-sugar for enhanced test output
-   ✅ pytest-xdist for parallel test execution
-   ✅ Ruff for fast Python linting and formatting
-   ✅ Comprehensive test structure

### Development Tools

-   ✅ Django Debug Toolbar (in DEBUG mode)
-   ✅ Django Browser Reload for auto-refresh
-   ✅ Django Extensions with management commands
-   ✅ Loguru for advanced logging
-   ✅ Environment variable management (django-environ, python-dotenv)

### Production Ready

-   ✅ WhiteNoise for static file serving
-   ✅ Security middleware configured
-   ✅ CSRF protection with trusted origins
-   ✅ Login required middleware
-   ✅ Ready for production deployment

## 📋 Prerequisites

-   Python 3.14 or higher
-   [uv](https://github.com/astral-sh/uv) package manager

## ⚡ Quick Start

For those who want to get running immediately:

```bash
# Clone and setup
git clone <repository-url> myproject && cd myproject

# Install dependencies
uv sync

# Setup database
uv run python manage.py migrate

# Create admin user
uv run python manage.py createsuperuser

# Run server
uv run python manage.py runserver
```

Visit `http://localhost:8000` - you're ready to build! 🚀

The homepage will display a welcome page with project information and quick links.

## 🔧 Detailed Setup

### 1. Clone or Use as Template

```bash
# Clone the repository
git clone <repository-url> your-project-name
cd your-project-name
```

### 2. Install Dependencies

```bash
# Using uv (recommended)
uv sync
```

### 3. Set Up Environment Variables

Create a `.env` file in the project root with your configuration:

```env
# Security
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite - default for development)
USE_SQLITE=True

# Database (PostgreSQL - for production)
# USE_SQLITE=False
# DB_NAME=your_database_name
# DB_USER=your_database_user
# DB_PASSWORD=your_database_password
# DB_HOST=localhost
# DB_PORT=5432
```

### 4. Run Migrations

```bash
uv run python manage.py migrate
```

### 5. Create Superuser

```bash
uv run python manage.py createsuperuser
```

### 6. Start Development Server

```bash
uv run python manage.py runserver
```

Visit `http://localhost:8000` to see your application running.

### 7. Access Django Admin

Use your superuser credentials to access the admin panel:

-   **Admin Panel**: `http://localhost:8000/admin/`

## 🎯 Pre-built Apps

### Users App

-   Custom User model extending Django's AbstractUser
-   User Profile model with phone number field
-   Automatic timestamp tracking (created/modified)
-   Author tracking (who created/modified)
-   Django admin integration

### Accounts App

-   Template-based authentication views:
    -   Login page with Django forms
    -   Registration/signup page
    -   Password change functionality
    -   Password reset flow (request and confirm)
    -   User profile management
-   Django Allauth integration for email verification
-   Session-based authentication
-   Optional REST API endpoints available (if API support is needed)

## 🐳 Docker Support

Build and run the application using Docker:

```bash
# Build the Docker image
docker build -t shirobase:latest .

# Run the container
docker run -p 8000:8000 --env-file .env shirobase:latest

# Run in detached mode
docker run -d -p 8000:8000 --env-file .env shirobase:latest

# Access running container
docker exec -it <container_id> sh
```

## 📦 Production Deployment

Before deploying to production:

```bash
# Set DEBUG=False in your .env file
DEBUG=False

# Collect static files
uv run python manage.py collectstatic --noinput

# Run migrations
uv run python manage.py migrate

# Create cache table (if using database cache)
uv run python manage.py createcachetable

# Check for common issues
uv run python manage.py check --deploy
```

## 🧪 Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov

# Run specific test file
uv run pytest path/to/test_file.py

# Run specific test Test Class
uv run pytest path/to/test_file.py::DummyTestClass

# Run specific test function
uv run pytest path/to/test_file.py::DummyTestClass::dummy_test_successful

# Run tests in parallel
uv run pytest -n auto
```

## 🎨 Code Quality

### Linting and Formatting

The project uses Ruff for fast linting and formatting:

```bash
# Check code for issues
uv run ruff check .

# Auto-fix issues
uv run ruff check --fix .

# Format code
uv run ruff format .
```

### Debug Tools

When `DEBUG=True`, the following tools are available:

-   **Debug Toolbar**: Visible on all pages, provides insights into queries, templates, cache, etc.
-   **Browser Reload**: Automatically refreshes the browser when code changes are detected

## 🛠️ Useful Management Commands

Django Extensions provides additional helpful commands:

```bash
# Show all URLs in the project
uv run python manage.py show_urls

# Generate UML diagram of models
uv run python manage.py graph_models -a -o models.png

# Run Django shell with auto-imports
uv run python manage.py shell_plus

# Clear all sessions
uv run python manage.py clear_cache

# Validate templates
uv run python manage.py validate_templates

# Show database info
uv run python manage.py sqlcreate

# Drop test database
uv run python manage.py drop_test_database
```

## 📦 Included Packages

This project comes pre-configured with:

### Authentication & Authorization

-   **django-allauth[socialaccount]** (v65.13.1+) - Complete authentication system with social auth support
-   **smartmin** (v5.2.2+) - Advanced permissions and user management
-   **dj-rest-auth** (v7.0.1+) - Optional REST API endpoints for authentication (if API support needed)
-   **djangorestframework-simplejwt** (v5.5.1+) - Optional JWT authentication tokens (if API support needed)

### Optional API Support

-   **djangorestframework** - Optional REST API toolkit (included but not primary focus)
-   **drf-spectacular** (v0.29.0+) - Optional OpenAPI 3.0 schema generation and Swagger UI
-   **django-filter** (v25.2+) - Optional dynamic QuerySet filtering for APIs

### Database & Models

-   **psycopg[binary]** (v3.2.12+) - PostgreSQL adapter for Python
-   **django-phonenumber-field[phonenumbers]** (v8.3.0+) - Phone number field with validation
-   **django-extensions** (v4.1+) - Custom management commands and model extensions
-   **django-author** (v1.2.0+) - Automatic created_by/modified_by tracking
-   **django-auditlog** (v3.3.0+) - Track model changes and user actions

### Development Tools

-   **django-debug-toolbar** (v6.1.0+) - Debug panel for Django applications
-   **django-browser-reload** (v1.21.0+) - Auto-reload browser on code changes
-   **ruff** (v0.14.6+) - Fast Python linter and formatter

### Testing

-   **pytest-django** (v4.11.1+) - Pytest plugin for Django
-   **pytest-sugar** (v1.1.1+) - Enhanced test output with progress bar
-   **pytest-xdist** (v3.8.0+) - Parallel test execution

### Utilities

-   **loguru** (v0.7.3+) - Simplified logging with advanced features
-   **django-environ** (v0.12.0+) - Environment variable management
-   **python-dotenv** (v1.2.1+) - Load environment variables from .env file
-   **whitenoise** (v6.11.0+) - Static file serving for production

## 🏗️ Project Structure

```
shirobase/
├── apps/                       # Django applications
│   ├── accounts/              # Authentication views and templates
│   ├── users/                 # Custom User model and Profile
│   └── api/                   # Optional REST API endpoints (if needed)
├── django_project/            # Main project configuration
│   ├── settings.py           # Project settings
│   ├── urls.py               # URL configuration
│   ├── middleware.py         # Custom middleware (CSRF handling)
│   ├── permissions.py        # Permission definitions
│   └── wsgi.py               # WSGI application
├── templates/                 # HTML templates
│   └── index.html            # Homepage template
├── static/                    # Static files (CSS, JS, images)
├── logs/                      # Application logs
├── pyproject.toml            # Project dependencies and metadata
├── uv.lock                   # Locked dependencies
├── pytest.ini                # Pytest configuration
├── ruff.toml                 # Ruff linter configuration
├── Dockerfile                # Docker container definition
├── entrypoint.sh            # Docker entrypoint script
├── manage.py                # Django management script
├── db.sqlite3               # SQLite database (development)
└── README.md                # This file
```

## ⚙️ Key Configuration

### Authentication Settings

The project is configured with:

-   **Custom User Model**: `apps.users.User` with email authentication
-   **Session Authentication**: Primary authentication method for template-based views
-   **Email Verification**: Optional (can be set to 'mandatory' or 'none')
-   **Login Methods**: Email-based authentication
-   **Django Allauth**: Complete authentication flows with templates
-   **Optional JWT**: JWT tokens available if REST API endpoints are used

### Middleware

Custom middleware included:

-   **CustomCsrfViewMiddleware**: Configurable CSRF protection (exempts URLs via `CSRF_EXEMPT_URLS`)
-   **LoginRequiredMiddleware**: Enforces authentication site-wide (configure exemptions as needed)
-   **WhiteNoiseMiddleware**: Serves static files efficiently in production
-   **AuditlogMiddleware**: Tracks all model changes automatically

### Logging

Loguru is configured to:

-   Write logs to `logs/shirobase.log`
-   Rotate log files at 10 MB
-   Retain logs for 10 days

### Static Files

-   Development: Served by Django
-   Production: Served by WhiteNoise
-   Static files directory: `static/`
-   Collected static files: `staticfiles/`

## 🎨 Customization

This is a skeleton project meant to be customized for your specific needs:

1. **Rename the project**: Update `django_project` folder and all references to match your application name
2. **Add your Django apps**: Create new apps in the `apps/` directory
3. **Create views and templates**: Build your views in app `views.py` files and templates in `templates/` directories
4. **Configure database**: Switch between SQLite (development) and PostgreSQL (production) via environment variables
5. **Customize authentication**: Extend the User and Profile models in `apps/users/models.py`
6. **Add permissions**: Define custom permissions in `django_project/permissions.py`
7. **Configure CSRF**: Add your domains to `CSRF_TRUSTED_ORIGINS` in settings
8. **Style your templates**: Update templates in `templates/` directory and add static files to `static/`
9. **Add business logic**: Build your features using the pre-configured foundation
10. **Enable API support**: If needed, REST API endpoints are available but not the primary focus

## 🔧 Troubleshooting

### Common Issues

**Issue: `ModuleNotFoundError` when running commands**

```bash
# Make sure you're using uv run before python commands
uv run python manage.py runserver
```

**Issue: Database migration conflicts**

```bash
# Reset migrations (development only!)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
uv run python manage.py makemigrations
uv run python manage.py migrate
```

**Issue: Static files not loading**

```bash
# Collect static files
uv run python manage.py collectstatic --noinput
```

**Issue: CSRF errors on forms**

-   Ensure CSRF tokens are included in your forms: `{% csrf_token %}`
-   Add your custom URL patterns to `CSRF_EXEMPT_URLS` in settings if needed
-   For API endpoints (if used), ensure they're prefixed with `/api` (configured in `CSRF_EXEMPT_URLS`)

**Issue: Login required on public pages**

-   Configure `LOGIN_EXEMPT_URLS` or modify `LoginRequiredMiddleware` behavior in settings
-   Use `@login_not_required` decorator on views that should be publicly accessible

## 🤝 Contributing

This is a base template project. Feel free to fork and customize it for your needs.

## 📝 License

-   MIT

## 🔮 Roadmap

Completed:

-   ✅ Pre-configured Django apps (users, accounts)
-   ✅ Docker configuration
-   ✅ Template-based authentication views
-   ✅ Multiple commonly used packages integrated
-   ✅ Optional REST API support (included but not primary)

Planned:

-   [ ] Add CI/CD pipeline examples (GitHub Actions, GitLab CI)
-   [ ] Celery integration for async tasks
-   [ ] Redis caching setup
-   [ ] Email template examples
-   [ ] Additional template examples and UI components
-   [ ] Production deployment guides (AWS, DigitalOcean, Railway)
-   [ ] Social authentication providers setup
-   [ ] File upload handling (S3/local storage)
-   [ ] Form handling examples
-   [ ] Monitoring and error tracking setup

## 📞 Support

For issues, questions, or contributions, please refer to the project's issue tracker.

---

**Built with ❤️ to accelerate Django web development**
