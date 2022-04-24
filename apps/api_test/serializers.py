from rest_framework import serializers

from .models import (Project, Host, Api, ApiRunRecord, Case, CaseArgument, ApiArgument, CaseRunRecord,
                     CaseApiRunRecord, CrontabTask)
from apps.api_auth.serializers import UserSerializer


class HostSerializer(serializers.ModelSerializer):
    project_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Host
        fields = ('id', 'name', 'project_id', 'host', 'description')


class ApiArgumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiArgument
        fields = '__all__'


class ApiSerializer(serializers.ModelSerializer):
    project_id = serializers.IntegerField(write_only=True)
    host = HostSerializer(read_only=True)
    host_id = serializers.IntegerField(write_only=True)
    arguments = ApiArgumentSerializer(many=True, read_only=True)

    class Meta:
        model = Api
        fields = '__all__'


class ApiRunRecordSerializer(serializers.ModelSerializer):
    api = ApiSerializer()

    class Meta:
        model = ApiRunRecord
        fields = '__all__'


class CaseArgumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseArgument
        exclude = ['case']


class CaseSerializer(serializers.ModelSerializer):
    project_id = serializers.IntegerField(write_only=True)
    apis = ApiSerializer(many=True, read_only=True)
    arguments = CaseArgumentSerializer(many=True, read_only=True)

    class Meta:
        model = Case
        exclude = ['user', 'project']


class CrontabTaskSerializer(serializers.ModelSerializer):
    project_id = serializers.IntegerField(write_only=True)
    case_id = serializers.IntegerField(write_only=True)
    case = CaseSerializer(read_only=True)
    expr = serializers.CharField(max_length=255)
    status = serializers.IntegerField(read_only=True)

    class Meta:
        model = CrontabTask
        fields = ['id', 'name', 'project_id', 'case_id', 'expr', 'status', 'case']


class ProjectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    last_update_time = serializers.DateTimeField(read_only=True)
    create_time = serializers.DateTimeField(read_only=True)
    user = UserSerializer(read_only=True)
    hosts = HostSerializer(many=True, read_only=True)
    apis = ApiSerializer(many=True, read_only=True)
    cases = CaseSerializer(many=True, read_only=True)
    tasks = CrontabTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = (
            'id', 'name', 'type', 'description', 'last_update_time', 'create_time', 'user', 'hosts', 'apis', 'cases',
            'tasks'
        )


class CaseApiRunRecordSerializer(serializers.ModelSerializer):
    api = ApiSerializer()

    class Meta:
        model = CaseApiRunRecord
        fields = '__all__'


class CaseRunRecordSerializer(serializers.ModelSerializer):
    api_records = CaseApiRunRecordSerializer(many=True)
    case = CaseSerializer()

    class Meta:
        model = CaseRunRecord
        fields = '__all__'
