# Payroll System Custom Skill

## Project Overview
Django-based payroll management system for schools with role-based access control (RBAC) and modular architecture.

## Tech Stack
- **Framework**: Django 4.2.30
- **Python**: 3.8.10
- **Database**: SQLite (default) / PostgreSQL (production)
- **PDF Generation**: WeasyPrint
- **QR Code**: qrcode library
- **Frontend**: Django templates + HTML/CSS

## Project Structure
```
payroll_system/
├── config/           # Django settings & URL routing
├── accounts/         # User authentication & RBAC
├── staff/           # Teacher & FixedStaff management
├── attendance/      # Attendance tracking & adjustments
├── payroll/         # Salary computation & payment sheets
├── templates/       # HTML templates
├── static/          # CSS & static files
├── manage.py        # Django management script
└── requirements.txt # Python dependencies
```

## Key Features
1. **Role-Based Access Control (RBAC)**: Principal, Discipline Master, Accountant, Proprietor, Teacher
2. **Attendance Tracking**: QR code scanning, manual adjustments
3. **Salary Computation**: Hourly rates, attendance-based calculations, adjustments
4. **Payment Sheets**: Generate, submit, approve, disburse
5. **PDF Exports**: Payment sheet PDFs with signatures
6. **Permission Matrix**: Strict separation of duties

## Development Commands
```bash
# Activate virtual environment
source venv/Scripts/Activate.ps1  # Windows PowerShell

# Run migrations
python manage.py migrate

# Load demo data
python manage.py seed_demo_data

# Start development server
python manage.py runserver

# Access admin panel
# URL: http://127.0.0.1:8000/admin/
# Admin: admin / admin123
```

## Demo Credentials
| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Superuser |
| principal | changeme123 | Principal |
| discipline | changeme123 | Discipline Master |
| accountant | changeme123 | Accountant |
| proprietor | changeme123 | Proprietor |
| teacher_demo | changeme123 | Teacher |

## Code Conventions
- Use `from __future__ import annotations` for Python 3.8 compatibility with type hints
- Implement business logic in `services.py`, not views
- Use `RoleRequiredMixin` for permission-based view access
- Models use Django ORM best practices (select_related, prefetch_related)

## Common Tasks

### Add a New Feature
1. Create models in `<app>/models.py`
2. Create forms in `<app>/forms.py`
3. Implement views/logic in `<app>/views.py`
4. Create templates in `templates/<app>/`
5. Wire up URLs in `<app>/urls.py`
6. Run migrations: `python manage.py makemigrations && python manage.py migrate`

### Create a New Django App
```bash
python manage.py startapp <app_name>
# Add to INSTALLED_APPS in config/settings.py
```

### Debug Tips
- Check role-based permissions in `accounts/permissions.py`
- View all routes: `python manage.py show_urls`
- Check database with: `python manage.py dbshell`
- Use `python manage.py shell` for interactive debugging

## Known Issues & Fixes
- **Python 3.8 Compatibility**: Use `from __future__ import annotations` for generic type hints (list[str], tuple[...])
- **WeasyPrint Dependencies**: System libraries (libpango, libgobject) may be missing on Windows - imports are conditionally loaded
- **Database**: psycopg2-binary excluded from requirements; add if using PostgreSQL

## UI UX PRO MAX Integration (v2.0)
An AI-powered design system for professional UI/UX across multiple platforms.

### Features
- **67 UI Styles**: Glassmorphism, Claymorphism, Minimalism, Brutalism, Neumorphism, Bento Grid, Dark Mode, AI-Native UI
- **161 Color Palettes**: Industry-specific, aligned with product types
- **57 Font Pairings**: Curated typography with Google Fonts
- **161 Reasoning Rules**: Industry-specific design system generation
- **25 Chart Types**: Dashboard/analytics recommendations
- **22 Tech Stacks**: React, Vue, Angular, Laravel, HTML+Tailwind, shadcn/ui, etc.
- **99 UX Guidelines**: Best practices and accessibility rules

### Payroll System Design Approach
**Industry Classification**: B2B Service (School Payroll Management)

**Recommended Style**: Modern Professional + Accessibility-First
- Clean, minimalist interface for productivity
- Clear hierarchy: Dashboard → Data Tables → Forms
- High contrast text (4.5:1 minimum) for accessibility
- Responsive: 375px (mobile), 768px (tablet), 1024px, 1440px

**Color Strategy**:
- Professional palette (not bright/neon)
- Clear status indicators: Green (approved), Yellow (pending), Red (rejected), Blue (info)
- Soft shadows + smooth transitions (200-300ms)
- Light mode primary with dark mode option

**Typography**:
- Headlines: Clean sans-serif (e.g., Inter, Poppins)
- Body: Readable sans-serif (e.g., Roboto, Open Sans)
- Data tables: Monospace for numbers (better readability)

**Key Components for Payroll**:
- Role-based dashboard layouts
- Data-dense tables with sorting/filtering
- Payment sheet preview with print-ready styling
- Form validation with clear error states
- Permission-aware UI (hide/show based on role)

**Anti-Patterns to Avoid**:
- ❌ No AI purple/pink gradients (looks generic)
- ❌ No harsh animations (productivity tool)
- ❌ No emoji icons (use SVG: Heroicons/Lucide)
- ❌ No missing focus states (keyboard navigation critical)
- ❌ No contrast issues (WCAG AA minimum)

**Pre-Delivery Checklist for Payroll UI**:
- [ ] All clickable elements: cursor-pointer
- [ ] Hover states: smooth transitions (150-300ms)
- [ ] Focus states: visible for keyboard users
- [ ] Dark mode: optional but suggested
- [ ] prefers-reduced-motion: respected
- [ ] Mobile responsive: tested at 375px, 768px, 1024px, 1440px
- [ ] Print styles: payment sheets legible when printed
- [ ] Permission states: visually distinct locked/disabled content

### Design System Command
```bash
# Generate design system for payroll
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "b2b school payroll management finance" --design-system -p "Payroll System"
```

## When Helping With This Project
- Always preserve RBAC separation of duties when modifying permissions
- Test with all user roles after permission changes
- Use services.py for business logic to keep it testable and reusable
- Consider impact on multiple roles when adding features
- Follow Django conventions: fat models, thin views, business logic in services
- Apply UI UX PRO MAX principles for professional, accessible, role-based interfaces
- Ensure print styles work for payment sheet PDF exports
- Maintain accessibility: contrast, focus states, keyboard navigation
