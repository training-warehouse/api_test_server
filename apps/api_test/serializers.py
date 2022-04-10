from rest_framework import serializers

from .models import Project, Host, Api, ApiRunRecord, Case, CaseArgument, ApiArgument
from apps.api_auth.serializers import UserSerializer


class HostSerializer(serializers.ModelSerializer):
    project_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Host
        fields = ('id', 'name', 'project_id', 'host', 'description')


class ApiSerializer(serializers.ModelSerializer):
    project_id = serializers.IntegerField(write_only=True)
    host = HostSerializer(read_only=True)
    host_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Api
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    last_update_time = serializers.DateTimeField(read_only=True)
    create_time = serializers.DateTimeField(read_only=True)
    user = UserSerializer(read_only=True)
    hosts = HostSerializer(many=True, read_only=True)
    apis = ApiSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'type', 'description', 'last_update_time', 'create_time', 'user', 'hosts', 'apis')


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
        exclude = ['user']
