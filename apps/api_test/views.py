from rest_framework.decorators import authentication_classes
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Project, Host, Api
from .serializers import ProjectSerializer, HostSerializer, ApiSerializer
from apps.api_auth.authorizations import JWTAuthentication


class ProjectView(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class HostViewSet(ModelViewSet):
    queryset = Host.objects.all()
    serializer_class = HostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class ApiViewSet(ModelViewSet):
    queryset = Api.objects.all()
    serializer_class = ApiSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
