from django.contrib.auth import get_user_model
from django.utils.timezone import now

from rest_framework.views import APIView, Response
from rest_framework.authtoken.serializers import AuthTokenSerializer

from .authorizations import generate_jwt
from .serializers import UserSerializer

User = get_user_model()


class LoginView(APIView):
    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            user.last_login = now()
            user.save()

            token = generate_jwt(user)
            user_serializer = UserSerializer(user)
            return Response(data={'token': token, 'user': user_serializer.data})
        else:
            return Response(data={'message': '数据提交错误'})
