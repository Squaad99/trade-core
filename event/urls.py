from django.urls import path
from event.views import EventStartView

urlpatterns = [
    path('start/<str:command>', EventStartView.as_view(), name='event-start'),
]

