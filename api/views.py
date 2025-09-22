from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import RegisterSerializer, UserSerializer, ClientSerializer, ProjectSerializer, TaskSerializer
from .models import Client, Project, Task
from .permissions import IsAdminOrReadOnly
from .utils.responses import success_response, error_response
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        print("Login attempt with:", attrs)  
        data = super().validate(attrs)
        return data
    @classmethod
    def get_token(cls, user):
        print("User here:", user)             
        token = super().get_token(user)
        token['email'] = user.email
        token['name'] = user.name
        token['role'] = user.role
        return token

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            return success_response(
                data=serializer.validated_data,
                message="Login successful",
                status_code=status.HTTP_200_OK
            )
        except Exception as e:
            return error_response(
                message="Invalid credentials. Please check email/password.",
                errors=str(e),
                status_code=status.HTTP_401_UNAUTHORIZED
            )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    print("request hrer coming", request.data)
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        return success_response(
            data={
                "user": UserSerializer(user).data,
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            },
            message="User registered successfully",
            status_code=status.HTTP_201_CREATED
        )
    return error_response(
        message="Registration failed",
        errors=serializer.errors,
        status_code=status.HTTP_400_BAD_REQUEST
    )

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-created_at')
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['role','is_active','is_staff']
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all().order_by('-created_at')
    serializer_class = ClientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status','company']
    permission_classes = [permissions.IsAuthenticated]


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    permission_classes = [permissions.IsAuthenticated]

    
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status','project_id','assignee_id']
    permission_classes = [permissions.IsAuthenticated]