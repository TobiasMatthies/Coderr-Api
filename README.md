# Coderr_Api

Welcome to Coderr_Api! This project is a Django REST Framework-based backend that provides an API for "Coderr", a demo-project inspired by fiverr.

Find the frontend here: https://github.com/Developer-Akademie-Backendkurs/project.Coderr

## Features

This API supports the following core features:

*   **User Management:** Authentication and management of user profiles.
*   **Offers:** Creating, viewing, and managing offers.
*   **Orders:** Processing orders for offers.
*   **Reviews:** Allowing users to leave reviews.
*   **Base Info:** Get general information used by other parts of the application.

## Getting Started

Follow this guide to set up a local development environment for the project.

### Prerequisites

Make sure you have Python 3.10 (or newer) and `pip` installed on your system.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/TobiasMatthies/Coderr-Api.git
    cd Coderr-Api
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv env

    # On macOS/Linux:
    source env/bin/activate

    # On Windows:
    # env\Scripts\activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the database migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Start the development server:**
    ```bash
    python manage.py runserver
    ```

The API should now be accessible at `http://127.0.0.1:8000/`.

## API Endpoints

The API endpoints are structured across different apps. Here is an overview of the available routes:

*   `/api/users/` - For user management and authentication (e.g., token creation).
*   `/api/offers/` - For creating, listing, retrieving, updating, and deleting offers.
*   `/api/orders/` - For managing orders.
*   `/api/reviews/` - For managing reviews.
*   `/api/base-info/` - For accessing base information.

The exact routes are defined in the `urls.py` files of the respective apps (`users/api/urls.py`, `offers/api/urls.py`, etc.).

## Built With

*   [Django](https://www.djangoproject.com/) - The web framework for perfectionists with deadlines.
*   [Django REST Framework](https://www.django-rest-framework.org/) - A powerful and flexible toolkit for building Web APIs.
*   [Simple JWT for Django REST Framework](https://django-rest-framework-simplejwt.readthedocs.io/) - For JSON Web Token authentication.
*   [django-filter](https://django-filter.readthedocs.io/en/stable/) - For filtering QuerySets.
*   [django-cors-headers](https://github.com/adamchainz/django-cors-headers) - For handling Cross-Origin Resource Sharing (CORS).
*   [SQLite](https://www.sqlite.org/index.html) - As the development database.
