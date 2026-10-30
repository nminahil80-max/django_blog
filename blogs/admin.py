from django.contrib import admin
from .models import Category, BlogPost

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','slug')
    search_fields=('name',)
    prepopulated_fields= {'slug':('name',)}
    
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display=('title','author','category','status','created_at')
    list_filter=('status', 'category')
    search_fields=('title','content','author__username')
    prepopulated_fields={'slug':('title',)}