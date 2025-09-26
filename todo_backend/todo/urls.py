from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TelegramAuthView, TaskViewSet, CategoryViewSet, UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/telegram/', TelegramAuthView.as_view(), name='telegram-auth'),
]