# WHERE DO I UPDATE WHAT?  (Project guide)

Everything is inside the `main/` folder, grouped by **topic** and by **role**
(Resident / Staff / Admin). You never need to search: use the tables below.

## 1. Folder map

```
barangay_system/
├── manage.py                    run commands (runserver, migrate ...)
├── GUIDE.md  README.md          this guide + setup steps
├── barangay/settings.py         DATABASE, EMAIL, time zone  (>>> EDIT markers inside)
└── main/
    ├── models/                  DATABASE TABLES
    │   ├── accounts.py            Resident, StaffProfile
    │   ├── documents.py           DocumentType, DocumentRequest, statuses, payment method
    │   └── barangay_setting.py    barangay name + QR Ph code (one row, edited in /admin/)
    ├── forms/                   FORMS (the fields people fill in)
    │   ├── auth_forms.py          login, resident sign-up, staff sign-up
    │   ├── resident_forms.py      document request form
    │   └── staff_forms.py         status/remarks form
    ├── views/                   PAGE LOGIC (what each page does)
    │   ├── auth.py                public pages + sends each role home
    │   ├── resident.py            RESIDENT pages
    │   ├── staff.py               STAFF pages
    │   └── admin_panel.py         ADMIN pages
    ├── urls/                    PAGE ADDRESSES (one file per role)
    │   ├── auth_urls.py  resident_urls.py  staff_urls.py  admin_urls.py
    ├── templates/               PAGE DESIGN (HTML)
    │   ├── base.html              sidebar/menu shown on every page
    │   ├── registration/          login.html, register.html, staff_register.html
    │   ├── resident/              RESIDENT pages
    │   ├── staff/                 STAFF pages
    │   ├── certificates/          one printable template per certificate (+ _base.html letterhead)
    │   ├── includes/              form_fields.html = how every form field is drawn
    │   └── manage/                ADMIN pages
    ├── static/css/style.css     COLORS and LOOK
    ├── certificates.py          which certificate template each document uses
    ├── document_defaults.py     the 20 documents residents can request
    ├── permissions.py           WHO can open what (resident / staff / admin)
    ├── checks.py                safety check: system only runs on MySQL
    ├── mail_backend.py          prints emails in the terminal safely (until real email is set up)
    ├── notifications.py         EMAIL wording
    ├── admin.py                 what shows in Django's /admin/
    └── management/commands/seed_documents.py   adds default document types
```

## 2. "I want to change ..." -> edit this

| I want to change | Edit |
|---|---|
| Menu / sidebar links, logo name, login time box | `templates/base.html` |
| Colors, sizes, fonts | `static/css/style.css` |
| Resident sign-up fields | `forms/auth_forms.py` (RegisterForm) **and** `models/accounts.py` (Resident) |
| Staff sign-up fields | `forms/auth_forms.py` (StaffRegisterForm) **and** `models/accounts.py` (StaffProfile) |
| Login rules / staff "waiting for approval" message | `forms/auth_forms.py` (EmailLoginForm) |
| What the resident sees (My Requests, New Request) | `templates/resident/` |
| Request form fields | `forms/resident_forms.py` (+ `models/documents.py` if adding a new field) |
| What staff see (list, manage request) | `templates/staff/` |
| The wording of a certificate | `templates/certificates/<certificate name>.html` (one file per certificate) |
| Certificate letterhead, signature lines, page layout (all certificates) | `templates/certificates/_base.html` |
| Which certificate prints for which document | `certificates.py` |
| Barangay name, officials, logos, certificate colour, QR Ph code | Admin sidebar > **Barangay Settings** (no code). The first QR is `static/img/default_qr_ph.png`, loaded by migration 0011 |
| Payment choices (Cash / QR Ph) | `models/documents.py` (METHODS) |
| Look of the whole system (background, sidebar, cards, buttons, fields: same design as login / sign-up) | `static/css/style.css` |
| Page title tile + icon on each page | `templates/includes/page_header.html` and `includes/icon.html` |
| How form fields are drawn | `templates/includes/form_fields.html` and `includes/field.html` |
| Sidebar menu, its title and highlighted link | `templates/base.html` |
| Request statuses (Pending, Ready ...) | `models/documents.py` (STATUS list) |
| Admin dashboard / staff approvals / user activity | `templates/manage/` and `views/admin_panel.py` |
| Email messages (confirmation, ready for pickup, approved) and who receives new-request emails | `notifications.py` |
| Barangay email inbox, Gmail login, MySQL password | `barangay/settings.py` (>>> EDIT markers) |
| Who can open which page | `permissions.py` |
| The list of documents (and their default fees) | `document_defaults.py`, then run `python manage.py seed_documents` |
| Change a fee / requirements | `/admin/` > Document types (no code) |
| Payment status (Unpaid / Paid / Free) | `models/documents.py` (PAYMENT), set by staff on the Manage page |

**After changing anything in `models/`** run:
`python manage.py makemigrations main` then `python manage.py migrate`.
Changes to forms, views, templates, CSS, emails: just save and refresh.

## 3. Pages by role

| Role | Pages (address) | Page files |
|---|---|---|
| Public | `/login/` `/register/` `/register/staff/` | `templates/registration/` |
| Resident | `/my/` `/request/new/` `/request/<id>/` | `views/resident.py` + `templates/resident/` |
| Staff | `/staff/` `/staff/request/<id>/` `/staff/request/<id>/print/` | `views/staff.py` + `templates/staff/` |
| Admin | `/manage/` `/manage/accounts/` (staff approvals) `/manage/users/` and `/admin/` | `views/admin_panel.py` + `templates/manage/` |

## 4. How to add a new page (always the same 4 steps)

1. Write the page logic in `views/<role>.py`  (use `@resident_required`, `@staff_required` or `@admin_required`).
2. Add its address in `urls/<role>_urls.py`.
3. Create its HTML in `templates/<role>/` (start with `{% extends "base.html" %}`).
4. Add a link to it in `templates/base.html` (sidebar).

## 5. Useful commands

```
python manage.py check_database      confirm MySQL is connected + show record counts
python manage.py migrate              create/update the MySQL tables
python manage.py createsuperuser      make the admin account
python manage.py seed_documents       re-add any missing default documents
python manage.py runserver            start the website
```
