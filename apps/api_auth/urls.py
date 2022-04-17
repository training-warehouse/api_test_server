from django.urls import path

from .views import LoginView, UserView, AvatarView

app_name = 'api_auth'

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('user', UserView.as_view(), name='user'),
    path('avatar', AvatarView.as_view(), name='avatar')
]
