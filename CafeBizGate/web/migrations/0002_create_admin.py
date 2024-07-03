from django.db import migrations
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

def create_admin(apps, schema_editor):
    Users = apps.get_model('web', 'Users')
    User = apps.get_model('auth', 'User')  # Import User model
    if not User.objects.filter(username='admin').exists():
        user = User.objects.create_user(username='admin', email='admin@gmail.com', password='admin')
        Users.objects.create(user=user, full_name='Admin User', phone_number='09123456789')

class Migration(migrations.Migration):

    dependencies = [
        # Your migration dependencies here
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_admin),
    ]

