from django.db import models
from django.conf import settings

class Category(models.TextChoices):
    MAINTENANCE = 'maintenance', 'Maintenance (Plumbing, etc.)'
    SAFETY = 'safety', 'Safety'
    GARBAGE = 'garbage', 'Garbage Collection'
    ELECTRICAL = 'electrical', 'Electrical Outages'
    OTHER = 'other', 'Other'

class Complaint(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.OTHER)
    society = models.ForeignKey('core.Society', on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photos = models.ManyToManyField('cloudinary_storage.MediaCloudinaryImage', blank=True)  # Wait, fix: Use ImageField for now
    # Wait, for MVP: Single photo
    photo = models.ImageField(upload_to='complaints/', blank=True)
    upvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='upvoted_complaints', blank=True)
    resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def upvote_count(self):
        return self.upvotes.count()

    def save(self, *args, **kwargs):
        # Auto-log
        super().save(*args, **kwargs)
        if self.pk:  # New/updated
            AuditLog.objects.create(
                user=self.created_by,
                action='complaint_updated',
                details={'complaint_id': self.pk, 'resolved': self.resolved}
            )

class Comment(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']