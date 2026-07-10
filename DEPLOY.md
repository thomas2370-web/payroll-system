# Deployment Guide: Render.com

## Step 1: Prepare Your Code
```bash
cd c:\Users\user\Music\payroll_system
git init
git add .
git commit -m "Initial commit - ready for deployment"
```

## Step 2: Push to GitHub (Required for Render)
1. Go to https://github.com/new
2. Create a new repository (e.g., `payroll-system`)
3. Run these commands:
```bash
git remote add origin https://github.com/YOUR_USERNAME/payroll-system.git
git branch -M main
git push -u origin main
```

## Step 3: Deploy on Render.com
1. Go to https://dashboard.render.com
2. Click "New +"
3. Select "Web Service"
4. Connect your GitHub repository
5. Fill in the form:
   - **Name**: `payroll-system`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - **Start Command**: `gunicorn config.wsgi:application`

## Step 4: Add Environment Variables
In Render dashboard, add these variables:
- **DJANGO_SECRET_KEY**: (auto-generated, don't worry)
- **DJANGO_DEBUG**: `False`
- **DJANGO_ALLOWED_HOSTS**: Your Render domain (e.g., `payroll-system.onrender.com`)

## Step 5: Add PostgreSQL Database
1. In Render, create a new "PostgreSQL" database
2. Render will set `DATABASE_URL` automatically
3. Your app will use it automatically via settings.py

## Important: Demo Data
After deployment, run this command to populate demo users:
- Go to Render Shell (in dashboard)
- Run: `python manage.py seed_demo_data`

OR do it locally before pushing:
```bash
python manage.py seed_demo_data
```

## Login Credentials After Deployment
- **principal** / thegame
- **discipline** / thegame
- **accountant** / thegame
- **proprietor** / thegame
- **teacher_demo** / thegame (select "Grace Manga" from list)

## Troubleshooting
- If database errors: Render PostgreSQL is running separately
- If static files missing: Already handled by WhiteNoise
- If images don't load: Check media files in Render's file system
