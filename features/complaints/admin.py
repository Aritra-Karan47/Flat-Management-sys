from django.contrib import admin
from .models import Complaint, Comment, Category

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'society', 'upvote_count', 'resolved', 'created_at']
    list_filter = ['category', 'resolved', 'society']
    readonly_fields = ['upvote_count']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['text', 'complaint', 'created_by', 'created_at']