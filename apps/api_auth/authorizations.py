from datetime import datetime, timedelta

import jwt
from jwt.exceptions import ExpiredSignatureError
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import exceptions

User = get_user_model()


def generate_jwt(user):
    expire_time = datetime.now() + timedelta(days=7)
    return jwt.encode({'userid': user.pk, 'exp': expire_time}, key=settings.SECRET_KEY)


class JWTAuthentication(BaseAuthentication):
    keyword = 'JWT'

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1 or len(auth) > 2:
            raise exceptions.AuthenticationFailed('不可用的JWT请求头')

        try:
            jwt_token = auth[1]
            jwt_info = jwt.decode(jwt_token, key=settings.SECRET_KEY, algorithms='HS256')
            user_id = jwt_info.get('userid')

            try:
                user = User.objects.filter(uid=user_id).first()
                return user, jwt_token
            except:
                raise exceptions.AuthenticationFailed('用户不存在')
        except ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('JWT Token 已过期')
