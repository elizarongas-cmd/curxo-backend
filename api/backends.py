from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


class EmailBackend(ModelBackend):
    """Authenticate using email instead of username"""
    def authenticate(self, request, username=None, password=None, **kwargs):
        email = kwargs.get('email', username)
        if email is None:
            return None
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None


class CookieJWTAuthentication(JWTAuthentication):
    """JWT authentication that reads tokens from httpOnly cookies"""

    def authenticate(self, request):
        header_result = super().authenticate(request)
        if header_result:
            return header_result

        access_token = request.COOKIES.get('access_token')
        if not access_token:
            return None

        try:
            validated_token = self.get_validated_token(access_token)
            return self.get_user(validated_token), validated_token
        except AuthenticationFailed:
            return None
