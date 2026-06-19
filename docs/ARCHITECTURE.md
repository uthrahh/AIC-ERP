# AIC-CIIC ERP — System Architecture

## Overview

AIC-CIIC ERP is a monolithic Django application using server-rendered templates (Bootstrap 5), PostgreSQL, and role-based access control for three actor types: **Public**, **Startup**, and **Admin**.

## Django App Structure

| App | Responsibility |
|-----|----------------|
| `accounts` | Custom User model, login/logout, password change, RBAC decorators |
| `startups` | Startup profiles, documents, team, public directory pages |
| `applications` | Public application form, admin review, print, approval email |
| `services` | Service requests, workflow, service feedback |
| `labs` | Labs, equipment, booking requests, approval workflow |
| `finance` | Invoices, payments, startup billing dashboard |
| `feedback` | Complaints and general feedback |
| `content` | Gallery, service offerings, incubation steps, sponsors (CMS) |
| `reports` | Admin analytics and export-ready report views |
| `audit` | Audit log model and middleware |
| `portal` | Public website pages, startup/admin home dashboards |

## Backend Layers

```
HTTP Request
    → Middleware (Security, WhiteNoise, Session, Auth, Audit, ProfileRequired)
    → URL Router (AIC-CIIC_erp/urls.py → app urls)
    → View (decorator-enforced RBAC)
    → Forms (validation)
    → Models (ORM / PostgreSQL)
    → Templates (Django + Bootstrap)
```

## Authentication & Authorization

- **Custom User** (`accounts.User`) with `role`: `admin` | `startup`
- **Startup linkage**: FK `User.startup → Startup`
- **Decorators**: `@admin_required`, `@startup_required`, `@role_required`
- **First-login gate**: `ProfileRequiredMiddleware` redirects incomplete startup profiles to setup
- **Django session** auth with 8-hour session timeout

## File Storage

- **Development**: `MEDIA_ROOT/media/` on local disk
- **Production**: Same path on server volume; recommend mounting persistent storage or S3-compatible backend (django-storages) for scale
- Upload paths: `startups/logos/`, `startups/documents/`, `gallery/`, etc.
- Access control enforced in views (startup sees own docs; admin sees all)

## Reporting Architecture

- ORM aggregations in `reports/views.py` (Count, Sum, Avg)
- Chart.js for public/admin dashboards
- Reports are admin-only; data queried live from transactional tables

## Workflow Automation

| Module | States | Automation |
|--------|--------|------------|
| Application | Pending → Complete → Under Review → Approved/Rejected | Email on approval |
| Service Request | New → Under Review → Processing → Closed | `closed_at` timestamp; feeds service logs |
| Lab Booking | New → Under Review → Approved/Rejected/Closed | Feeds lab usage history |
| Invoice | Draft → Sent → Partial → Paid/Overdue | Auto status on payment record |

## Database

19 tables (core 17 + StartupTeamMember + StartupMedia):

`users`, `startups`, `documents`, `applications`, `application_reviews`, `service_requests`, `service_feedback`, `labs`, `equipment`, `lab_bookings`, `booking_equipment`, `complaints`, `general_feedback`, `invoices`, `payments`, `gallery`, `audit_logs`, plus CMS tables.

All startup FK relationships use `ON DELETE CASCADE`.

## Security

- CSRF on all forms
- Password validators (Django defaults)
- Role checks on every protected view
- Audit logging for critical actions
- Production settings: SSL, secure cookies, HSTS (when `DEBUG=False`)

## Deployment Topology

```
[Nginx] → [Gunicorn] → [Django App]
              ↓
         [PostgreSQL]
              ↓
         [Media Volume]
```

## Scaling Notes

- Designed for 1 admin + 250 startup users
- PostgreSQL connection pooling (pgBouncer) recommended at scale
- Static files via WhiteNoise; CDN optional
- Background email: swap to Celery + Redis for high volume
