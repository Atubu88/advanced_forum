import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myforum.settings')

application = get_wsgi_application()

# Добавьте эту строку в конце файла
app = application
