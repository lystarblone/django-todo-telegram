from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Category, Task

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'is_staff')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'due_date', 'created_at')
    list_filter = ('categories', 'user')
    search_fields = ('title', 'description')
    raw_id_fields = ('user',)