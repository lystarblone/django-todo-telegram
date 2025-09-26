from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from .models import Task, Category, CustomUser
from .serializers import TaskSerializer, CategorySerializer, UserSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class TelegramAuthView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        telegram_id = request.data.get('telegram_id')
        if not telegram_id:
            return Response({"detail": "Telegram ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        user, created = CustomUser.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={'username': f'user_{telegram_id}', 'email': f'user_{telegram_id}@example.com'}
        )
        
        token, _ = Token.objects.get_or_create(user=user)
        
        return Response({
            "token": token.key,
            "user_id": user.username
        }, status=status.HTTP_200_OK)