# Barangay Document Request System (Django + MySQL)

See **GUIDE.md** to find which file to edit for any change.

## Setup
1. Start MySQL (XAMPP / WAMP / MySQL Server) and create the database:
       CREATE DATABASE barangay_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
2. Open `barangay/settings.py` and set your MySQL user/password (or set DB_USER / DB_PASSWORD).
3. Install and build the tables:
       python -m venv venv
       venv\Scripts\activate          (Mac/Linux: source venv/bin/activate)
       pip install -r requirements.txt
       python manage.py migrate
       python manage.py check_database      <- confirms the MySQL connection
       python manage.py createsuperuser     <- this is the ADMIN account
       python manage.py runserver
4. Open http://127.0.0.1:8000  and log in as the admin.
5. Log in as admin and click **Barangay Settings** in the left menu. (Same page as Admin Panel > Barangay settings.) and fill in the barangay name, municipality, province and
   Punong Barangay (printed on every certificate). Your MariBank QR Ph code is already added by `migrate`;
   to use a different QR, upload a new one in the same place. Without any QR, residents can only choose Cash.
6. The 20 barangay documents are added automatically by `migrate`. Each has a low default fee
   (0 to 200 pesos, estimates). Confirm them with your barangay and change any fee in Admin Panel > Document types. (`python manage.py seed_documents` re-adds any you deleted.)

## Payment
- Residents choose **Cash** (pay at the Barangay Hall) or **Pay online via QR Ph** when they request a document.
- QR Ph: they scan the barangay's QR code with GCash, Maya or any bank app, then upload the receipt screenshot and
  reference number. Staff check it and mark the request **Paid**. (The system does not confirm payments by itself.)

## Certificates
Staff open a request > **Print Certificate**. Each of the 20 documents has its own wording in
`main/templates/certificates/`. Click the text on the print page to edit or fill in blanks before printing.

## Roles
- **Resident**: signs up and can use the system right away (no approval), logs in with email, requests documents, tracks status.
- **Staff**: signs up at /register/staff/ (admin approves), manages requests, prints documents.
- **Admin**: approves staff accounts only, sees dashboard and last logins. Staff can also be created
  directly in /admin/ (Users > Add user > tick "Staff status") and need no approval.

## Emails
Emails print in the terminal by default. For real emails (Gmail): turn on 2-step verification,
create an App Password, then set EMAIL_HOST_USER, EMAIL_HOST_PASSWORD and BARANGAY_EMAIL
(use `set` on Windows, `export` on Mac/Linux).
Sent automatically: new request (to the barangay inbox AND every approved staff member + confirmation to the resident), staff account approved/rejected,
request Approved / Rejected / Ready for Pickup (to the resident, signed with the name of the staff who handled it), new staff sign-up waiting (to barangay).
