from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email: raise ValueError("Users must have an email")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password: user.set_password(password)
        else: user.set_unusable_password()
        user.save(using=self._db); return user
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True); extra_fields.setdefault('is_superuser', True); extra_fields.setdefault('role','admin')
        return self.create_user(email, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=120, blank=True)
    role = models.CharField(max_length=30, default='user')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    def save(self,*a,**k):
        self.updated_at = timezone.now()
        super().save(*a,**k)
    def __str__(self): return self.email
class Client(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=40, blank=True, null=True)
    company = models.CharField(max_length=120, blank=True, null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    class Meta: db_table='clients'
    def save(self,*a,**k): self.updated_at=timezone.now(); super().save(*a,**k)
class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, default='todo')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    class Meta: db_table='projects'
    def save(self,*a,**k): self.updated_at=timezone.now(); super().save(*a,**k)
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, default='todo')
    due_date = models.DateTimeField(blank=True, null=True)
    assignee_id = models.IntegerField(blank=True, null=True)
    project_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    class Meta: db_table='tasks'
    def save(self,*a,**k): self.updated_at=timezone.now(); super().save(*a,**k)