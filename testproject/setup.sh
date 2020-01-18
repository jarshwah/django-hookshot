#!/bin/bash
set -euo pipefail

python application.py migrate --no-input
python application.py collectstatic --no-input

cat <<EOF | python application.py shell
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.filter(username="admin").first()
if user:
    user.set_password("admin")
    user.save()
else:
    User.objects.create_superuser('admin', 'admin@myproject.com', 'admin')
EOF

echo "superuser created with username:admin and password:admin"
echo "Start the server with python application.py runserver <port?>"
