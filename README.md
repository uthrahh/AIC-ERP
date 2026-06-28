# AIC ERP
## Project Documentation & Handover Guide

---

# Project Information

## Project Title

Startup Incubation & Resource Management ERP (AIC–CIIC ERP)

## Description

The Startup Incubation & Resource Management ERP is a centralized web-based platform developed to digitize the operational workflows of the Crescent Innovation & Incubation Council (CIIC). The system replaces manual processes carried out through spreadsheets, emails and WhatsApp with a role-based ERP that manages startup onboarding, incubation, resource allocation, laboratory and conference hall bookings, service requests, finance, mentorship and administrative operations.

The platform is designed for multiple stakeholders including Public Users, Applicants, Startups, Mentors and Administrators.

## Framework

Django

## Developed By

Pavithra Uthrah R. K. - uthrahrk@gmail.com

---

# Technology Stack

## Backend

- Python 3
- Django
- Django ORM

## Frontend

- HTML5
- Bootstrap 5
- Django Templates
- JavaScript

## Database

- PostgreSQL
- SQLite (Development)

## Libraries

- Pillow
- OpenPyXL
- ReportLab
- Pandas

---

# Features

## Authentication

- Role-based authentication
- Admin login
- Startup login
- Mentor login
- Applicant login

## Startup Applications

- Online application submission
- Application review
- Approval / Rejection
- Status tracking
- Printable application

## Startup Management

- Startup profiles
- Founder information
- Documents
- Financial information
- Team members
- Awards
- IPR
- Social media
- Bank details

## Laboratory Management

- Lab management
- Equipment management
- Equipment master import
- Lab booking
- Booking approval
- Calendar view

## Conference Hall

- Hall management
- Booking management
- Calendar

## Services

- Service requests
- Request tracking

## Finance

- Invoice models
- Payment models
- Billing foundation

## Feedback

- Complaints
- Feedback management

## Audit

- Activity logging

---

# Project Structure

```text
AIC-ERP/
│
├── accounts/
├── applications/
├── audit/
├── feedback/
├── finance/
├── halls/
├── labs/
├── mentors/
├── mentorship/
├── portal/
├── services/
├── startups/
├── templates/
├── static/
├── media/
├── manage.py
├── requirements.txt
└── README.md
```

---

# Installation Guide

## 1. Clone Repository

```bash
git clone <repository-url>
cd AIC-ERP
```

## 2. Create Virtual Environment

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure Database

Update database configuration in:

```
settings.py
```

or

```
.env
```

## 5. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## 6. Create Superuser

```bash
python manage.py createsuperuser
```

## 7. Run the Application

```bash
python manage.py runserver 8080
```

Open:

```
http://127.0.0.1:8080
```

---

# Running the System

Start the development server

```bash
python manage.py runserver 8080
```

Useful commands

```bash
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py shell
python manage.py collectstatic
python manage.py createsuperuser
python manage.py import_equipment
```

---

# Modules

- Public Website
- User & Role Management
- Startup Applications
- Startup Management
- Laboratory Management
- Equipment Management
- Conference Hall Management
- Service Management
- Finance
- Feedback & Complaints
- Audit Logs

---

# Completed

- Authentication & RBAC
- Public website
- Startup application workflow
- Startup management
- Lab booking
- Equipment management
- Equipment Excel import
- Conference hall booking
- Service requests
- Audit logging
- Basic finance models
- Dashboard foundation

---

# Pending

- Payment gateway integration
- Automated billing
- Quarterly financial updates
- Mentor scheduling workflow
- Advanced analytics dashboards
- Report generation (PDF/Excel)
- Email reminder scheduler
- Dynamic tariff engine
- Production deployment

---

# License

This project was developed during an internship at the Crescent Innovation & Incubation Council (CIIC) for internal startup incubation and resource management.
