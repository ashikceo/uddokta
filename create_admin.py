import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
# Change 'admin' and 'your_secure_password' to whatever credentials you want
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@uddoktardokan.com', 'your_secure_password')
    print("Superuser created successfully!")
else:
    print("Superuser already exists.")
