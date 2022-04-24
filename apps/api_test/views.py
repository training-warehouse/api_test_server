from rest_framework.views import APIView, Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import (Project, Host, Api, ApiRunRecord, Case, CaseArgument, ApiArgument, CaseRunRecord,
                     CaseApiRunRecord, CrontabTask)
from .serializers import (ProjectSerializer, HostSerializer, ApiSerializer, ApiRunRecordSerializer,
                          CaseArgumentSerializer, CaseSerializer, CaseRunRecordSerializer, CrontabTaskSerializer)
from apps.api_auth.authorizations import JWTAuthentication
from . import api_request
from .view_extension import run_case
from . import api_scheduler


class IndexView(APIView):
    def get(self, request):
        project_count = Project.objects.count()
        api_count = Api.objects.count()
        case_count = Case.objects.count()
        api_record_count = ApiRunRecord.objects.count()
        case_record_count = CaseApiRunRecord.objects.count()

        data = {
            'count': {
                'project': project_count,
                'api': api_count,
                'case': case_count,
                'api_record': api_record_count,
                'case_record': case_record_count
            }
        }
        return Response(data)


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
                            # fixme ApiArgument不应该挂在api上
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

    def put(self, request, case_id):
        serializer = CaseSerializer(data=request.data)
        if serializer.is_valid():
            name = request.data.get('name')
            arguments = request.data.get('arguments')
            apis = request.data.get('apis')
            description = request.data.get('description')

            case = Case.objects.get(pk=case_id)
            case.name = name
            case.description = description

            if arguments:
                argument_models = []
                for argument in arguments:
                    argument_id = argument['id']
                    if argument_id:
                        argument_mod = CaseArgument.objects.get(pk=argument_id)
                        argument_mod.name = argument['name']
                        argument_mod.value = argument['value']
                        argument_mod.save()
                    else:
                        argument_mod = CaseArgument.objects.create(
                            name=argument['name'],
                            value=argument['value'],
                            case=case
                        )
                    argument_models.append(argument_mod)
                case.arguments.set(argument_models)
            else:
                case.arguments.set([])

            if apis:
                api_models = []
                for api in apis:
                    api_mod = Api.objects.get(pk=api['id'])

                    api_arguments = api['arguments']
                    if api_arguments:
                        argument_models = []
                        for api_argument in api_arguments:
                            argument_id = api_argument['id']
                            if argument_id:
                                argument_mod = ApiArgument.objects.get(pk=argument_id)
                                argument_mod.name = api_argument['name']
                                argument_mod.origin = api_argument['origin']
                                argument_mod.format = api_argument['format']
                                argument_mod.save()
                            else:
                                argument_mod = ApiArgument.objects.create(
                                    name=api_argument['name'],
                                    origin=api_argument['origin'],
                                    format=api_argument['format'],
                                    case=case
                                )
                            argument_models.append(argument_mod)
                        api_mod.arguments.set(argument_models)
                    else:
                        api_mod.arguments.set([])

                    api_mod.save()
                    api_models.append(api_mod)

                case.apis.set(api_models)
            else:
                case.apis.set([])

            case.save()
            return Response(CaseSerializer(case).data)
        else:
            print(serializer.errors)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RunCaseView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, case_id):
        case_record = run_case(case_id, request)

        serializer = CaseRunRecordSerializer(case_record)
        return Response(serializer.data)


class RecordView(APIView):
    def get(self, request):
        record_type = request.GET.get('type')
        project_id = request.GET.get('project')
        if record_type == 'api':
            records = ApiRunRecord.objects.filter(api__project_id=project_id)
            serializers = ApiRunRecordSerializer(records, many=True)
        else:
            records = CaseRunRecord.objects.filter(case__project_id=project_id)
            serializers = CaseRunRecordSerializer(records, many=True)

        return Response(serializers.data)


class CrontabTaskView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializers = CrontabTaskSerializer(data=request.data)
        if serializers.is_valid():
            name = serializers.validated_data.get('name')
            project_id = serializers.validated_data.get('project_id')
            case_id = serializers.validated_data.get('case_id')
            expr = serializers.validated_data.get('expr')

            task = CrontabTask.objects.create(name=name, project_id=project_id, case_id=case_id, expr=expr,
                                              user=request.user)
            return Response(CrontabTaskSerializer(task).data)
        else:
            print(serializers.errors)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, task_id):
        serializers = CrontabTaskSerializer(data=request.data)
        if serializers.is_valid():
            name = serializers.validated_data.get('name')
            case_id = serializers.validated_data.get('case_id')
            expr = serializers.validated_data.get('expr')

            queryset = CrontabTask.objects.filter(pk=task_id)
            queryset.update(name=name, case_id=case_id, expr=expr)
            return Response(CrontabTaskSerializer(queryset.first()).data)
        else:
            print(serializers.errors)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class StartStopTaskView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, task_id, target_status):
        task = CrontabTask.objects.get(pk=task_id)
        if target_status == 1:
            if task.status == 1:
                # task正在运行
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'task 正在运行，无需再次启动'})
            api_scheduler.add_task(task, request)
            task.status = 1
        elif target_status == 2:
            if task.status == 2:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'task 没有在运行，不需要停止'})
            api_scheduler.remove_task(task)
            task.status = 2
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': '状态值不符合规范'})
        task.save()
        return Response(CrontabTaskSerializer(task).data)
