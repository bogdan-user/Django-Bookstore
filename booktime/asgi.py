import os
import django
from channels.routing import get_default_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'booktime.settings')

django.setup()

application = get_default_application()


#DEVELOPMENT
# import os
#
# from django.core.asgi import get_asgi_application
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'booktime.settings')
#
# application = get_asgi_application()
