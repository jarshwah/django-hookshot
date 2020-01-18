from rest_framework.routers import DefaultRouter
from django.conf.urls import url

from .views import HookShotView, HookListView

app_name = "hookshot"
urlpatterns = [
    url(r"(?P<hook_name>[-_\w]+)/$", HookShotView.as_view(), name="hookshot"),
    url(r"$", HookListView.as_view(), name="hookshot-list"),
]
