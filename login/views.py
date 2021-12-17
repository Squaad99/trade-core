import os

from django.contrib.auth.views import LoginView


# Create your views here.
class UserLoginView(LoginView):
    template_name = os.path.join("login.html")


class UserLogoutView(LoginView):
    template_name = os.path.join("logout.html")
