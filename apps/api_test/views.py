from rest_framework.views import APIView, Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Project, Host, Api, ApiRunRecord, Case, CaseArgument, ApiArgument
from .serializers import (ProjectSerializer, HostSerializer, ApiSerializer, ApiRunRecordSerializer,
                          CaseArgumentSerializer, CaseSerializer)
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


class CaseView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CaseSerializer(data=request.data)
        if serializer.is_valid():
            name = request.data.get('name')
            arguments = request.data.get('arguments')
            apis = request.data.get('apis')
            description = request.data.get('description')
            project_id = request.data.get('project_id')

            case = Case.objects.create(
                name=name,
                description=description,
                user=request.user,
                project_id=project_id
            )

            if arguments:
                for argument in arguments:
                    CaseArgument.objects.create(
                        name=argument['name'],
                        value=argument['value'],
                        case=case
                    )

            if apis:
                apis.sort(key=lambda x: x['index'])
                for api in apis:
                    api_mod = Api.objects.get(pk=api['id'])
                    case.apis.add(api_mod)
                    api_arguments = api['arguments']
                    if api_arguments:
                        for api_argument in api_arguments:
                            ApiArgument.objects.create(
                                name=api_argument['name'],
                                origin=api_argument['origin'],
                                format=api_argument['format'],
                                api=api_mod
                            )
            case.save()
            return Response(CaseSerializer(case).data)
        else:
            print(serializer.errors)
            return Response(status=status.HTTP_400_BAD_REQUEST)
