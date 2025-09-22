from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Client, Project, Task
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering=('email',)
    list_display=('email','name','role','is_active','is_staff','created_at')
    fieldsets=( (None,{'fields':('email','password')}),('Info',{'fields':('name','role')}),('Permissions',{'fields':('is_active','is_staff','is_superuser','groups','user_permissions')}),('Dates',{'fields':('last_login','created_at','updated_at')}) )
    add_fieldsets=((None,{'classes':('wide',),'fields':('email','name','role','password1','password2','is_staff','is_superuser')}),)
    search_fields=('email','name'); readonly_fields=('created_at','updated_at')
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display=('name','email','phone','company','status','created_at')
    search_fields=('name','email','phone','company'); list_filter=('status',); readonly_fields=('created_at','updated_at')
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display=('name','status','created_at'); search_fields=('name','description','status'); list_filter=('status',); readonly_fields=('created_at','updated_at')
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display=('title','status','due_date','project_id','assignee_id'); search_fields=('title','description','status'); list_filter=('status',); readonly_fields=('created_at','updated_at')