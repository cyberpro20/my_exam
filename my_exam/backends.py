from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

class EmailOrPhoneModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            validate_email(username)
            user = UserModel.objects.get(email=username)
        except (UserModel.DoesNotExist, ValidationError):
            try:
                user = UserModel.objects.get(mobile=username)
            except UserModel.DoesNotExist:
                return None

        if user.check_password(password):
            return user
        return None
