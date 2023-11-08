from django.db import models
from .model_user import UserModel


class BlacklistedTokenModel(models.Model):
    token = models.TextField()
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    def blacklist_token(token):
        BlacklistedTokenModel.objects.create(token=token)

    def is_token_blacklisted(token):
        return BlacklistedTokenModel.objects.filter(token=token).exists()
