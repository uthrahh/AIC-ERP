# AIC-CIIC ERP — UI/UX Wireframes

## Design System

- **Framework**: Bootstrap 5.3
- **Primary color**: `#1a5276` (AIC-CIIC blue)
- **Typography**: Segoe UI / system sans-serif
- **Components**: Cards with soft shadow, badge status indicators, responsive tables

---

## Public Site

### Home
```
[Navbar: About | Gallery | Startups | Dashboard | Apply | Contact | Login]
[Hero: AIC-CIIC title + Apply / Explore CTAs]
[3 stat cards: Startups | Domains | Portal Access]
[Horizontal marquee: Featured startup logos + names]
[Footer: Contact info]
```

### About
```
[Description paragraph - placeholder]
[Services grid 2-col: title + one-line description]
[Process timeline: Step badges 1-6 with cards]
```

### Gallery
```
[Horizontal auto-scroll row: 10 image cards + caption]
```

### Startup Directory
```
[Title]                    [Search bar ────────── 🔍]
[3-row horizontal marquee of startup cards]
  Each card: logo | name | tagline → links to public profile
```

### Startup Public Profile
```
[Logo centered]
[Company Name + tagline]
[Description]
[Team grid]
[Media gallery]
[Contact: email | phone]
```

### Public Dashboard
```
[4 KPI cards: Startups | Funding | Domains | Sponsors]
[Pie chart: domain-wise startups]
[Bar chart: year-wise startups]
[Sponsor list]
```

### Application Form
```
Multi-section form:
  Founder info | Startup info | Problem/Solution
  Support checkboxes | Submit button
```

### Contact
```
[Phone | Email | Office address cards]
```

---

## Startup Portal

### Home (post-login)
```
Welcome, {Company} (ID: XXXX)
[Open Requests | Complaints | Paid | Outstanding]
[Latest services table]     [Quick actions sidebar]
```

### Request Service
```
Dropdown: Electricity | AC | Manpower | Others
Description textarea → Submit
```

### Schedule Lab
```
Lab dropdown | Date | Start/End time | Equipment checkboxes
```

### Profile
```
Company details | Edit | Upload docs
Service Logs table (auto from closed requests)
Lab History table (auto from approved bookings)
Funding dashboard
Help: Complaint | Feedback | Contact links
```

---

## Admin Portal

### Home
```
[3 alert cards: New Services | New Applications | New Complaints]
[Quick links row: Create Startup | Applications | Services | Labs | Finance | Reports]
[3 columns: Recent services | applications | complaints]
```

### Application Review
```
Left: Application details
Right: Review form (scores 1-10, comments, HOD, department, status)
[Print button → signature lines for Founder | HOD | CTO]
```

### Service / Lab Management
```
Filterable table → Detail page with status dropdown + assign/approve
```

### Reports
```
Dashboard KPIs → Sub-reports:
  Startups | Services | Labs | Finance | Feedback
```

---

## Status Color Coding

| Status | Badge |
|--------|-------|
| New / Pending | Secondary |
| Under Review | Info |
| Processing / Approved | Primary |
| Closed / Paid | Success |
| Rejected / Overdue | Danger |

---

## Responsive Behavior

- Navbar collapses to hamburger on mobile
- Tables scroll horizontally on small screens
- Dashboard charts stack vertically on mobile
- Marquee animations pause-friendly (CSS infinite scroll)
