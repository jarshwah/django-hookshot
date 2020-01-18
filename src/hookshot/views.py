from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.exceptions import NotFound
from rest_framework.permissions import BasePermission, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .registry import _registry, webhook


class HookTokenPermission(BasePermission):
    def has_permission(self, request, view):
        return super().has_permission(request, view)


class HookListView(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication]

    def get(self, request):
        return Response({name: hookargs.description for name, hookargs in _registry.items()})


class HookShotView(APIView):
    permission_classes = []
    authentication_classes = []

    def _get_hook(self, request, hook_name):
        hook_args = _registry.get(hook_name)
        if hook_args is None:
            raise NotFound(detail="No hook exists at {}".format(hook_name))
        return hook_args

    def verify_access(self, request, hook_args):
        if hook_args.insecure:
            return
        # unit tests may force authentication
        if len(request.authenticators) == 0:
            request.authenticators = [TokenAuthentication()]
        request._authenticate()
        HookTokenPermission().has_permission(request, self)

    def check_permissions(self, request):
        return super().check_permissions(request)

    def prepare(self, request, hook_name):
        hook_args = self._get_hook(request, hook_name)
        self.verify_access(request, hook_args)
        func = hook_args.func
        bound = func.__get__(self, HookShotView)
        return bound

    def post(self, request, hook_name, **kwargs):
        bound = self.prepare(request, hook_name)
        return bound(request, **kwargs)

    def get(self, request, hook_name, **kwargs):
        bound = self.prepare(request, hook_name)
        return bound(request, **kwargs)
