# BCIT Accreditation System

A system for managing and analyzing BCIT Engineering program accreditation data, allowing faculty to upload student assessment data and generate analytics reports.

## Table of Contents
- [System Overview](#system-overview)
- [Local Development Setup](#local-development-setup)
- [Docker Deployment](#docker-deployment)
- [Production Deployment](#production-deployment)
- [Database Management](#database-management)
- [Troubleshooting](#troubleshooting)

## System Overview

The BCIT Accreditation System is a web application built with Django that helps manage engineering program accreditation data. It provides:

- Secure form-based data upload for assessment information
- Student assessment data management
- Analytics dashboard for program assessment
- Admin tools for data management
- Export functionality for reporting

- Make sure that PostgresSQL is set to port 1047

## Local Development Setup

### Prerequisites
- Python 3.11+
- PostgreSQL 14+
- Git

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd proj1047-accreditation-db
   ```
2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up the database**
   - Create a new PostgreSQL database and user for the project.
   - Update the `DATABASES` setting in `backend/bcit_accreditation/settings.py` with your database information.
   - Run migrations: `cd backend && python manage.py migrate`

5. **Run the development server**
   ```bash
   cd backend && python manage.py runserver
   ```
   Access the application at `http://127.0.0.1:8000/`.

## Docker Deployment

### Prerequisites
- Docker and Docker Compose installed
- Git to clone the repository

### Deployment Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd proj1047-accreditation-db
   ```

2. **Create a .env file**
   Create a file named `.env` in the project root directory with the following content:
   ```
   DB_NAME=accreditation_db
   DB_USER=basic_user
   DB_PASSWORD=proj1047
   ALLOWED_HOSTS=localhost,127.0.0.1
   DEBUG=False
   SECRET_KEY=your-secure-secret-key-here
   FERNET_KEY=VFKv0OBwXRxMR9n10hFGm3ExTxcCNs3g7DHxsFn3mEc=
   ```
   
   Note: For production, be sure to:
   - Replace the ALLOWED_HOSTS with your actual server domain or IP
   - Generate a secure Django SECRET_KEY 
   - Generate a secure FERNET_KEY using: `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`

3. **Build and start the Docker containers**
   ```bash
   docker-compose build
   docker-compose up -d
   ```

4. **Verify the containers are running**
   ```bash
   docker-compose ps
   ```
   All services should show as "Up" with their respective ports mapped.

5. **Create a Django superuser (admin)**
   ```bash
   docker-compose exec web bash -c "cd backend && python manage.py createsuperuser"
   ```
   Follow the prompts to create an admin username, email, and password.

6. **Access the application**
   - Web application: http://localhost:8000
   - With Nginx: http://localhost (port 80)
   - Admin interface: http://localhost/admin (login with the superuser credentials)

### Additional Docker Commands

- **View logs** (useful for troubleshooting):
  ```bash
  docker-compose logs
  ```
  Or for a specific service:
  ```bash
  docker-compose logs web
  ```

- **Stop the services**:
  ```bash
  docker-compose down
  ```

- **Stop and remove all containers, networks, and volumes**:
  ```bash
  docker-compose down -v
  ```

- **Restart the services after making changes**:
  ```bash
  docker-compose restart
  ```

## Production Deployment

### Server Requirements
- Ubuntu 20.04+
- PostgreSQL 14+
- Python 3.11+

### Deployment Steps

1. **Update and upgrade the server**
   ```bash
   sudo apt update
   sudo apt upgrade
   ```
2. **Install PostgreSQL**
   ```bash
   sudo apt install postgresql postgresql-contrib
   ```
3. **Create a PostgreSQL database and user**
   ```bash
   sudo -u postgres psql
   CREATE DATABASE accreditation_db;
   CREATE USER basic_user WITH PASSWORD 'proj1047';
   ALTER ROLE basic_user SET client_encoding TO 'utf8';
   ALTER ROLE basic_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE basic_user SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE accreditation_db TO basic_user;
   \q
   ```
4. **Clone the repository and install dependencies**
   ```bash
   git clone <repository-url>
   cd proj1047-accreditation-db
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
5. **Configure the application**
   - Update the `DATABASES` setting in `backend/bcit_accreditation/settings.py` with your database information.
   - Set `DEBUG = False` in `backend/bcit_accreditation/settings.py`.
   - Add your domain to the `ALLOWED_HOSTS` list in `backend/bcit_accreditation/settings.py`.

6. **Run migrations and collect static files**
   ```bash
   cd backend && python manage.py migrate
   cd backend && python manage.py collectstatic
   ```
7. **Set up a systemd service for Gunicorn**
   ```ini   [Unit]
   Description=gunicorn daemon for bcit_accreditation
   After=network.target

   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/path/to/proj1047-accreditation-db/backend
   ExecStart=/path/to/proj1047-accreditation-db/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/path/to/proj1047-accreditation-db/bcit_accreditation.sock bcit_accreditation.wsgi:application

   [Install]
   WantedBy=multi-user.target
   ```
8. **Start and enable the Gunicorn service**
   ```bash
   sudo systemctl start bcit_accreditation
   sudo systemctl enable bcit_accreditation
   ```
9. **Set up Nginx**
   ```bash
   sudo apt install nginx
   ```
   Create a new Nginx server block configuration file:   ```nginx
   server {
       listen 80;
       server_name your_domain.com;

       location = /favicon.ico { access_log off; log_not_found off; }
       location /static/ {
           root /path/to/proj1047-accreditation-db/backend;
       }

       location / {
           include proxy_params;
           proxy_pass http://unix:/path/to/proj1047-accreditation-db/bcit_accreditation.sock;
       }
   }
   ```
   Enable the new server block configuration:
   ```bash
   sudo ln -s /etc/nginx/sites-available/bcit_accreditation /etc/nginx/sites-enabled
   sudo nginx -t
   sudo systemctl restart nginx
   ```

## Database Management

- Use Django's built-in admin interface for managing database records.
- Regularly back up the database using `pg_dump` and `pg_restore`.

## Troubleshooting

- For permission denied errors, ensure the correct file and directory permissions are set for the web server user.
- Check the logs for Gunicorn and Nginx for error messages and troubleshooting information.
- Ensure the virtual environment is activated when installing dependencies or running management commands.