import eventlet.wsgi
import eventlet
import socketio
import os
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

sio = socketio.Server(
    async_mode='eventlet',
    cors_allowed_origins=os.getenv(
        "CORS_ALLOWED_ORIGINS",
        "http://localhost:3000"
    ).split(",")
)

django_app = StaticFilesHandler(get_wsgi_application())
application = socketio.WSGIApp(sio, django_app)

# Start server
eventlet.wsgi.server(eventlet.listen(('', 8000)), application)