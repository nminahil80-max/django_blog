from django.contrib import admin

from .models import Comment, Like

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=('user','blog','created_at')
    search_fields= ('content','user__username', 'blog_title')
    list_filter=('created_at',)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display=('user','blog','created_at')
    search_fields=('user__username', 'blog_title')
    list_filter=('created_at',)