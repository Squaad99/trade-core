from django.urls import path

from api_app.views import TestApiView

urlpatterns = [
    path('event-start/', TestApiView.as_view())
]