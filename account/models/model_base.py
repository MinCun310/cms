import datetime
from django.db import models

app_name = 'account'

class BaseModel(models.Model):
    
    deleted_at = models.DateTimeField(null=True)
    
    def soft_delete(self):
        self.deleted_at = datetime.datetime.now()
        self.save()
        
    def restore(self):
        self.deleted_at = None
        self.save()
        
    class Meta:
        abstract = True