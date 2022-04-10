from rest_framework.views import APIView, Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Project, Host, Api, ApiRunRecord
from .serializers import ProjectSerializer, HostSerializer, ApiSerializer, ApiRunRecordSerializer
from apps.api_auth.authorizations import JWTAuthentication
from . import api_request


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


class RunApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, api_id):
        api = Api.objects.get(pk=api_id)
        resp = api_request.request(api)

        record = ApiRunRecord.objects.create(
            url=resp.url,
            http_method=resp.request.method,
            return_code=resp.status_code,
            return_content=resp.text,
            data=resp.request.body,
            headers=api.headers,
            api=api,
            user=request.user
        )

        serializer = ApiRunRecordSerializer(record)
        return Response(serializer.data)
