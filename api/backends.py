from django.contrib.auth import get_user_model

User = get_user_model()

class EmailBackend:
    def authenticate(self, request, username=None, password=None, **kwargs):
        email = kwargs.get('email', username)
        if email is None:
            return None
        try:
            # Use our custom Usuario model
            from api.models import Usuario
            user = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            from api.models import Usuario
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None
