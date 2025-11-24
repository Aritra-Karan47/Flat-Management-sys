from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class Society(models.Model):
    name = models.CharField(max_length=200, unique=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Societies"

    def __str__(self):
        return self.name

class User(AbstractUser):
    # ensure email exists and is unique if you use it as USERNAME_FIELD
    email = models.EmailField('email address', unique=True)

    phone = models.CharField(max_length=15, unique=True, blank=True)
    society = models.ForeignKey(Society, on_delete=models.SET_NULL, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_resident = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'  # Login by email
    REQUIRED_FIELDS = ['username', 'phone']  # include username when USERNAME_FIELD != 'username'

    def __str__(self):
        return f"{self.email} ({self.phone})"

class AuditLog(models.Model):  # Track actions (e.g., complaint raised)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)  # e.g., "complaint_created"
    details = models.JSONField(default=dict)  # Flexible: {"complaint_id": 1}
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']