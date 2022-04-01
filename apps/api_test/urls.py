from rest_framework.routers import DefaultRouter

from .views import ProjectView, HostViewSet, ApiViewSet

app_name = 'api_test'

router = DefaultRouter(trailing_slash=False)
router.register('project', ProjectView, basename='project')
router.register('host', HostViewSet, basename='host')
router.register('api', ApiViewSet, basename='api')

urlpatterns = [] + router.urls
