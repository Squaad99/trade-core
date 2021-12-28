from django.urls import path
from event.views import EventListView, SchedulerStartView

urlpatterns = [
    path('start/<str:command>', EventListView.as_view(), name='event-list'),
    path('scheduler-start/<str:command>', SchedulerStartView.as_view(), name='scheduler-start'),
]