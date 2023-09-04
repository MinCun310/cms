from django.db import models
from .model_base import BaseModel
from .model_user import UserModel

class DeviceModel(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    useragent = models.TextField(max_length=500)
    ip = models.CharField(max_length=255)
    session_id = models.CharField(max_length=255, null=True)
    extra_info = models.JSONField()
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)