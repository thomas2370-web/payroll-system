# Cloud-Based QR Attendance and Payroll Management System

Django implementation for Collège Bilingue Charles de Gaulle. The core
workflow is implemented end-to-end in the codebase: teacher registration →
QR-based attendance → disciplinary adjustments → salary computation →
payment-sheet approval → teacher sign-off → PDF export.

## Current project status

Implemented so far:
- Role-based authentication and navigation for Principal, Discipline Master,
  Accountant, Proprietor, and Teacher users.
- Teacher and fixed-staff management, including QR code generation for teachers.
- Attendance check-in/check-out flow with penalty/adjustment handling.
- Payroll sheet generation, submission, approval/rejection, and signing.
- Payslip and payment-sheet PDF export.
- Demo seed data and starter templates for the main workflow.

Still pending or planned:
- A proper automated test suite.
- Stronger QR security controls (rotation, identity checks, anti-fraud safeguards).
- Production hardening such as environment-based deployment settings and
  database/configuration review.
- Additional reporting, audit, and UX refinements.

This README will be updated whenever a major feature or workflow change is
made.

## Quick start

```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py seed_demo_data   # creates one login per role
python manage.py runserver
```

Open http://127.0.0.1:8000 and log in with any of:

| Username        | Role              | Password     |
|-----------------|-------------------|--------------|
| principal       | Principal         | changeme123  |
| discipline      | Discipline Master | changeme123  |
| accountant      | Accountant        | changeme123  |
| proprietor      | Proprietor        | changeme123  |
| teacher_demo    | Teacher           | changeme123  |

Also run `python manage.py createsuperuser` if you want full Django admin
access at `/admin/`.

**⚠️ Change or remove `seed_demo_data` before deploying to production** —
it creates known-password accounts for evaluation only.

## Trying the full workflow

1. Log in as **principal** → "Register teacher" → fill the form. A QR
   code is generated automatically (view it from the teacher list).
2. Log in as **discipline** → "Scan QR" → paste the teacher's QR token
   (visible on their QR page, or use a real camera — the scan page uses
   `html5-qrcode` and will request camera permission) → Check in, then
   later Check out. Apply a penalty from "Attendance log" if needed.
3. Log in as **accountant** → "Payment sheets" → generate a sheet for
   the current month → Submit for approval.
4. Log in as **proprietor** → open the sheet → Approve (or reject with
   a reason, which sends it back to the Accountant).
5. Log in as **teacher_demo** → "My payslips" → confirm receipt & sign.
   Once every entry on a sheet is signed, its status flips to DISBURSED
   automatically.
6. Download the signed payment sheet as a PDF from the sheet detail page.

## Project layout

- `accounts/` — custom `User` model with `role`, RBAC decorators/mixins
- `staff/` — `Teacher` (with auto QR generation) and `FixedStaff`
- `attendance/` — check-in/out records, disciplinary `Adjustment`
  (justification is mandatory and enforced at the model level)
- `payroll/` — `PaymentSheet` / `SalaryEntry`, the approval state machine
  in `services.py`, and PDF export in `pdf.py`

## Notes for going to production

- Switch `DATABASES` in `config/settings.py` to PostgreSQL (the driver
  is already in `requirements.txt`).
- Set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, and `DJANGO_ALLOWED_HOSTS`
  as environment variables.
- The QR-fraud mitigation discussed in the project report (static QR =
  shareable like an ID badge) is not yet implemented — consider adding
  a visual identity check step for the Discipline Master, or rotating
  tokens, before relying on this for a real payroll cycle.
- No automated test suite is included yet — the `smoke_test.py` script
  used during development (not included here) exercised the full
  workflow via Django's test client; consider turning that into a
  proper `pytest`/`TestCase` suite.

## Claude CLI

A minimal CLI to call Anthropic Claude from this project. It uses the
REST endpoint and requires an environment variable `ANTHROPIC_API_KEY`.

1. Set your key (PowerShell temporary):

```powershell
$env:ANTHROPIC_API_KEY = "sk-..."
python claude_cli.py --prompt "Hello Claude"
```

2. Or make it persistent (Windows):

```powershell
setx ANTHROPIC_API_KEY "sk-..."
# restart terminal to pick up setx changes
```

You can override the model with `--model` or the endpoint with `--endpoint`.

