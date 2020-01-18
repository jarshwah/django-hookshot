"""
isort:skip_file
"""
import django
import sys
from django.conf import settings
from django.core.handlers.wsgi import WSGIHandler
from django.core.management import execute_from_command_line  # new
from pathlib import Path

HERE = Path(__file__).resolve()
HERE_DIR = HERE.parent

hookshot_path = HERE.parents[1] / "src" / "hookshot"
assert hookshot_path.exists(), "Couldn't add hookshot to PYTHONPATH"

sys.path.insert(0, hookshot_path)

settings.configure(
    ROOT_URLCONF=__name__,
    SECRET_KEY="v0=invbm^_8=dz+dn4&oz+dkruoz8j$ehqq&j*mit-t%a&cvz=",
    DEBUG=True,
    STATIC_URL="/static/",
    STATIC_ROOT=HERE_DIR / "collected",
    INSTALLED_APPS=[
        "hookshot",
        "rest_framework",
        "rest_framework.authtoken",
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
    ],
    MIDDLEWARE=[
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
    ],
    DATABASES=dict(default=dict(ENGINE="django.db.backends.sqlite3", NAME="database.sqlite3")),
    TEMPLATES=[
        dict(
            BACKEND="django.template.backends.django.DjangoTemplates",
            OPTIONS=dict(
                context_processors=[
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
                loaders=[
                    "django.template.loaders.filesystem.Loader",
                    "django.template.loaders.app_directories.Loader",
                ],
            ),
        )
    ],
    REST_FRAMEWORK=dict(DEFAULT_AUTHENTICATION_CLASSES=[],),
)

django.setup()

from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from hookshot import urls as hookshot_urls
from hookshot.registry import webhook
from rest_framework.response import Response


def hello_world(request):
    return HttpResponse("Hello, Django!")


@webhook("hello_webhook", description="Returns Hello")
def hello_webhook(self, request):
    return Response(dict(result="secure hello"))


@webhook("insecure_webhook", description="No auth required")
def insecure_webhook(self, request):
    return Response(dict(result="insecure hello"))


@webhook("my_hook", description="Name doesn't match function name")
def random_name(self, request):
    return Response(dict(result="random hello"))


urlpatterns = [
    path("admin/", admin.site.urls),
    path("webhooks/", include(hookshot_urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("", hello_world),
]

application = WSGIHandler()

if __name__ == "__main__":  # new
    execute_from_command_line()
