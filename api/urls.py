from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView
from .views import register, LoginView, UserViewSet, ClientViewSet, ProjectViewSet, TaskViewSet
from . import datatable as dt
router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'clients', ClientViewSet, basename='client')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'tasks', TaskViewSet, basename='task')
urlpatterns = [
    path('auth/register', register, name='register'),
    path('auth/login', LoginView.as_view(), name='login'),
    path('auth/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
    path('datatable/users', dt.UsersDT.as_view()),
    path('datatable/clients', dt.ClientsDT.as_view()),
    path('datatable/projects', dt.ProjectsDT.as_view()),
    path('datatable/tasks', dt.TasksDT.as_view()),
]