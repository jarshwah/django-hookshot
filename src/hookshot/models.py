from django.db import models

# from django.utils import timezone
# from hookshot.registry import RegistryChoices


# A CharField that doesn't migrate choices
class CharField(models.CharField):
    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        # Ignore choice changes when generating migrations
        kwargs.pop("choices", None)
        return (name, path, args, kwargs)


# TODO: add a management command to sync hooks table

# class Webhook(models.Model):
#     HOOKS = RegistryChoices()
#     name = CharField(max_length=200, unique=True, choices=HOOKS)
#     description = models.CharField(max_length=200)
#     installed = models.DateTimeField(default=timezone.now, editable=False)


# class WebhookPermission(models.Model):
#     token = models.ForeignKey(
#         "restframework.authtoken.Token",
#         on_delete=models.CASCADE,
#         help_text="The auth token to grant hook permissions to",
#     )
#     allowed_webhooks = models.ManyToManyField(
#         Webhook, help_text="Which webhooks is this token allowed to call"
#     )
