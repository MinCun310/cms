from django.db import models
from django.contrib.auth.models import AbstractUser
from ..config import MYROLE
import uuid

app_name='account'

def get_random_string(string_length=10):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4()) # Convert UUID format to a Python string.
    random = random.upper() # Make all characters uppercase.
    random = random.replace("-","") # Remove the UUID '-'.
    return random[0:string_length] # Return the random string.

class UserModel(AbstractUser):
    first_name = models.CharField(max_length=15, null=True)
    last_name = models.CharField(max_length=15, null=True)
    email = models.EmailField(max_length=50, unique=True, null=True)
    email_verified_at = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=15, null=True)
    phone_verified_at = models.CharField(max_length=50, null=True)
    avatar = models.CharField(max_length=255, null=True)
    role = models.SmallIntegerField(default=MYROLE['MEMBER'])
    two_fa_enable_at = models.DateTimeField(null=True)
    two_fa_secret = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []
    
    class Meta:
        app_label = 'account'
        managed = True
        db_table = 'user'
        ordering = ['-created_at', '-updated_at', '-id']
        indexes = [
            models.Index(fields=['email', 'id']),
        ]
        
    def save(self, *args, **kwargs):
        """
            Khi tạo 1 user mới, thì thay đổi username, email thành viết thường
        """
        if not self.id:
            self.username = self.email.split('@')[0]
            self.username = self.username.lower()
            if self.email:
                self.email = self.email.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
    
# class OldPasswords(models.Model):
#     user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
#     pwd = models.CharField(max_length=200)
    