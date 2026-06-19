# AIC-CIIC ERP

Full-stack ERP for the **Centre for Innovation, Incubation & Entrepreneurship (AIC-CIIC)** — startup incubation management, service requests, lab scheduling, finance, feedback, and public portal.

## Tech Stack

- **Backend**: Django 6 + Python 3.11+
- **Frontend**: Django Templates + Bootstrap 5 + Chart.js
- **Database**: PostgreSQL (production) / SQLite (local dev default)
- **Auth**: Django sessions + role-based access (Admin / Startup)

## Features

| Module | Capabilities |
|--------|-------------|
| Public Portal | About, Gallery, Startup Directory (140+), Dashboard, Application, Contact |
| Applications | Submit, review, approve/reject, print with signatures, approval email |
| Startup Portal | Profile setup, service requests, lab booking, billing, complaints, feedback |
| Admin Portal | Create startups, manage workflows, finance, reports, history |
| Finance | Invoices, partial payments, billing dashboard |
| Audit | Activity logging for critical operations |

## Quick Start (Development)

### 1. Prerequisites

- Python 3.11 or 3.13
- PostgreSQL 14+ (optional — SQLite works for local dev)
- Git

### 2. Clone & Install

```bash
git clone <your-repo-url> AIC-CIIC-ERP
cd AIC-CIIC-ERP
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Environment Configuration

```bash
copy .env.example .env   # Windows
# cp .env.example .env   # macOS/Linux
```

Edit `.env` — for quick local dev, defaults use SQLite (no PostgreSQL needed).

### 4. Database Setup

```bash
python manage.py migrate
python manage.py seed_data
python manage.py collectstatic --noinput
```

### 5. Run Server

```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000**

### Default Login Credentials (after seed)

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin12345` |
| Demo Startup | `startup_demo` | `startup12345` |

> Change all passwords before production deployment.

---

## PostgreSQL Setup (Production / Staging)

### 1. Create Database

```sql
CREATE DATABASE AIC-CIIC_erp;
CREATE USER AIC-CIIC_user WITH PASSWORD 'strong_password_here';
GRANT ALL PRIVILEGES ON DATABASE AIC-CIIC_erp TO AIC-CIIC_user;
```

### 2. Update `.env`

```env
DEBUG=False
SECRET_KEY=generate-a-long-random-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

DB_ENGINE=django.db.backends.postgresql
DB_NAME=AIC-CIIC_erp
DB_USER=AIC-CIIC_user
DB_PASSWORD=strong_password_here
DB_HOST=localhost
DB_PORT=5432

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=AIC-CIIC@yourdomain.com
```

### 3. Migrate & Seed

```bash
python manage.py migrate
python manage.py seed_data
python manage.py createsuperuser   # optional extra superuser
```

---

## Production Deployment (Linux + Nginx + Gunicorn)

### 1. Server Preparation

```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx postgresql postgresql-contrib
```

### 2. Deploy Application

```bash
sudo mkdir -p /var/www/AIC-CIIC-erp
sudo chown $USER:$USER /var/www/AIC-CIIC-erp
cd /var/www/AIC-CIIC-erp
git clone <repo> .
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with production values
python manage.py migrate
python manage.py seed_data
python manage.py collectstatic --noinput
mkdir -p media logs
```

### 3. Gunicorn Systemd Service

Create `/etc/systemd/system/AIC-CIIC-erp.service`:

```ini
[Unit]
Description=AIC-CIIC ERP Gunicorn
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/AIC-CIIC-erp
Environment="PATH=/var/www/AIC-CIIC-erp/venv/bin"
ExecStart=/var/www/AIC-CIIC-erp/venv/bin/gunicorn AIC-CIIC_erp.wsgi:application \
    --bind 127.0.0.1:8001 --workers 3 --timeout 120
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable AIC-CIIC-erp
sudo systemctl start AIC-CIIC-erp
```

### 4. Nginx Configuration

Create `/etc/nginx/sites-available/AIC-CIIC-erp`:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    client_max_body_size 10M;

    location /static/ {
        alias /var/www/AIC-CIIC-erp/staticfiles/;
    }

    location /media/ {
        alias /var/www/AIC-CIIC-erp/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/AIC-CIIC-erp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 5. SSL (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

### 6. Backup Strategy

**Database (daily cron):**

```bash
pg_dump -U AIC-CIIC_user AIC-CIIC_erp > /backups/AIC-CIIC_erp_$(date +%Y%m%d).sql
```

**Media files:**

```bash
tar -czf /backups/AIC-CIIC_media_$(date +%Y%m%d).tar.gz /var/www/AIC-CIIC-erp/media/
```

---

## Project Structure

```
AIC-CIIC-ERP/
├── AIC-CIIC_erp/          # Project settings & root URLs
├── accounts/          # Authentication & users
├── startups/          # Startup profiles & documents
├── applications/      # Incubation applications
├── services/          # Service requests
├── labs/              # Lab scheduling
├── finance/           # Invoices & payments
├── feedback/          # Complaints & feedback
├── content/           # Gallery, CMS content
├── reports/           # Analytics & reports
├── audit/             # Audit logging
├── portal/            # Public & dashboard pages
├── templates/         # HTML templates
├── static/            # CSS, JS
├── media/             # Uploaded files
└── docs/              # Architecture & wireframes
```

## Key URLs

| URL | Description |
|-----|-------------|
| `/` | Public home |
| `/about/` | About AIC-CIIC |
| `/startups/` | Startup directory |
| `/dashboard/` | Public stats dashboard |
| `/applications/submit/` | Application form |
| `/accounts/login/` | Login |
| `/AIC-CIIC-admin/` | Admin dashboard |
| `/startup/` | Startup dashboard |
| `/admin/` | Django superuser admin |

## Running Tests

```bash
python manage.py test
```

## Documentation

- [System Architecture](docs/ARCHITECTURE.md)
- [UI Wireframes](docs/WIREFRAMES.md)

## Admin Workflows

1. **Create Startup**: Admin → Create Startup → generates ID + login credentials
2. **Review Application**: Applications → Review → Approve sends email
3. **Service Request**: Startup submits → Admin updates status → Closed → optional feedback
4. **Lab Booking**: Startup books → Admin approves/rejects
5. **Finance**: Admin creates invoice → records payments → startup views billing

## Security Checklist (Production)

- [ ] Set `DEBUG=False`
- [ ] Use strong `SECRET_KEY`
- [ ] Configure PostgreSQL with limited-privilege user
- [ ] Enable HTTPS
- [ ] Change default seed passwords
- [ ] Configure SMTP for real emails
- [ ] Set up automated backups
- [ ] Restrict `/admin/` access by IP if needed

## License

Proprietary — AIC-CIIC Internal Use
