from django.urls import path
from django_q.models import Schedule

from event.views import EventListView, TestEventsView
from manage import RUN_MODE

urlpatterns = [
    path('start/<str:command>', EventListView.as_view(), name='event-list'),
    path('test-buy-and-sell/<str:command>', TestEventsView.as_view(), name='test-events'),
]

if RUN_MODE:
    name = "Buy and place orders"
    existing_schedule = Schedule.objects.filter(name=name)
    if not existing_schedule:
        schedule = Schedule(name=name, func='event.tasks.buy_and_place_orders_job',
                            schedule_type=Schedule.CRON,
                            cron='0 15 * * 1-5',
                            repeats=-1,
                            args="'prod'")
        schedule.save()

    name = "Check orders and transactions"
    existing_schedule = Schedule.objects.filter(name=name)
    if not existing_schedule:
        schedule = Schedule(name=name, func='event.tasks.check_transactions_and_orders_job',
                            schedule_type=Schedule.CRON,
                            cron='0 19 * * 1-5',
                            repeats=-1,
                            args="'prod'")
        schedule.save()
