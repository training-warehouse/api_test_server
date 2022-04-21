from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (ProjectView, HostViewSet, ApiViewSet, RunApiView, CaseView, RunCaseView, RecordView, IndexView,
                    CrontabTaskView)

app_name = 'api_test'

router = DefaultRouter(trailing_slash=False)
router.register('project', ProjectView, basename='project')
router.register('host', HostViewSet, basename='host')
router.register('api', ApiViewSet, basename='api')

urlpatterns = [
                  path('index', IndexView.as_view(), name='index'),
                  path('run/api/<int:api_id>', RunApiView.as_view(), name='run_api'),
                  path('run/case/<int:case_id>', RunCaseView.as_view(), name='run_case'),
                  path('case', CaseView.as_view(), name='case'),
                  path('case/<int:case_id>', CaseView.as_view(), name='edit_case'),
                  path('record', RecordView.as_view(), name='record'),
                  path('task', CrontabTaskView.as_view(), name='task'),
                  path('task/<int:task_id>', CrontabTaskView.as_view(), name='add_task'),
              ] + router.urls
