from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = MyUser.objects.get(username=username)
        if user and user.check_password(password):
            return user
        return None


# from django.contrib.auth.backends import BaseBackend

# from .models import MyUser
# class MyBackend(BaseBackend):
#     def authenticate(self, request, username=None, password=None):
#         user = MyUser.objects.get(username=username)
#         if user and user.check_password(password):
#             return user
#         return None