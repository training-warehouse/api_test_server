from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ProjectView, HostViewSet, ApiViewSet, RunApiView

app_name = 'api_test'

router = DefaultRouter(trailing_slash=False)
router.register('project', ProjectView, basename='project')
router.register('host', HostViewSet, basename='host')
router.register('api', ApiViewSet, basename='api')

urlpatterns = [
                  path('run/api/<int:api_id>', RunApiView.as_view(), name='run_api')
              ] + router.urls
