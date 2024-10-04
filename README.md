# Dental Management System

This is a Django-based Dental Management System designed to manage patients, doctors, appointments, and procedures efficiently.

## Setup Instructions

### Prerequisites

- Python
- Django
- PostgreSQL

### Installation

1. **Clone the repository**:
   - git clone https://github.com/AditVirkar/Dental_management.git
   - cd dental-management

2. **Create a virtual environment**:
   - python -m venv env
   - source env/bin/activate  # For Linux/Mac
   - env\Scripts\activate     # For Windows

3. **Install dependencies**:
   #### Install Django
   pip3 install django

   #### Install psycopg2 for PostgreSQL support
   pip3 install psycopg2-binary


4. **Apply migrations**:
   python manage.py migrate

5. **Create a superuser**:
   python manage.py createsuperuser

6. **Run the development server**:
   python manage.py runserver

## Features

- **Doctor and Patient Management**: Manage doctors, patients, and their respective details.
- **Appointments**: Schedule and manage appointments between patients and doctors.
- **Procedures**: Add and update medical procedures and their associated details.
- **Address and Contact Information**: Manage contact details for both patients and doctors.
- **Schedules**: Handle working schedules of doctors.
- **Migrations**: All database changes are handled by Django migrations.

## API Endpoints

- **Admin Panel**: /admin/
- **Homepage**: /
