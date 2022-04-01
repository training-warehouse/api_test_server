from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

User = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('uid', 'telephone', 'username', 'email', 'avatar', 'date_joined', 'is_active')
