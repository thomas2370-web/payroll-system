#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Update passwords for all demo users
users = User.objects.filter(username__in=['principal', 'discipline', 'accountant', 'proprietor', 'teacher_demo'])
for user in users:
    user.set_password('thegame')
    user.save()
    print(f"✓ Updated {user.username} password to 'thegame'")

print(f"\nTotal users updated: {users.count()}")
