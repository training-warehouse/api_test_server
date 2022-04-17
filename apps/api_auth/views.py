import os

import shortuuid
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.timezone import now

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response
from rest_framework.authtoken.serializers import AuthTokenSerializer

from .authorizations import generate_jwt, JWTAuthentication
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


class UserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def put(self, request):
        user = request.user

        user.username = request.data.get('username')
        user.telephone = request.data.get('telephone')
        user.email = request.data.get('email')
        user.avatar = request.data.get('avatar')
        user.save()

        return Response(UserSerializer(user).data)


class AvatarView(APIView):
    @staticmethod
    def save_file(file):
        # abc.jpg => ('abc','.jpg')
        filename = shortuuid.uuid() + os.path.splitext(file.name)[-1]
        with open(os.path.join(settings.MEDIA_ROOT, filename), 'wb') as fp:
            for chunk in file.chunks():
                fp.write(chunk)
        return settings.MEDIA_URL + filename

    def post(self, request):
        file = request.FILES.get('file')
        filepath = self.save_file(file)

        filepath = request.build_absolute_uri(filepath)
        return Response({'picture': filepath})
