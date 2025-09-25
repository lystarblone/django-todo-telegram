from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginView, TaskViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', LoginView.as_view(), name='login'),
]