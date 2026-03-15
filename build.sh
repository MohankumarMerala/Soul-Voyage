set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@soulavoyage.com', 'Admin@1234')
    print('Superuser created successfully')
else:
    print('Superuser already exists:', User.objects.filter(is_superuser=True).values('username'))
"
