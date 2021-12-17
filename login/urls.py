import os

from django.urls import path

from login.views import UserLoginView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', UserLoginView.as_view(), name='login'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name=os.path.join('logout.html')), name='logout'),
]