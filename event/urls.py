from django.urls import path
from django_q.models import Schedule

from event.views import EventListView, TestEventsView
from manage import RUN_MODE

urlpatterns = [
    path('start/<str:command>', EventListView.as_view(), name='event-list'),
    path('test-buy-and-sell/<str:command>', TestEventsView.as_view(), name='test-events'),
]

if RUN_MODE:
    # test_job_name = "Test job"
    # existing_test_job = Schedule.objects.filter(name=test_job_name)
    # if not existing_test_job:
    #     test_job_schedule = Schedule(name=test_job_name, func='event.tasks.test_job', schedule_type=Schedule.MINUTES,
    #                                  minutes=1, repeats=-1)
    #     test_job_schedule.save()

    health_check_name = "Health check job"
    existing_health_check_job = Schedule.objects.filter(name=health_check_name)
    if not existing_health_check_job:
        health_check_schedule = Schedule(name=health_check_name, func='event.tasks.health_check_job',
                                         schedule_type=Schedule.CRON,
                                         cron='0 */6 * * *', repeats=-1)
        health_check_schedule.save()

    name = "Buy and place orders"
    existing_schedule = Schedule.objects.filter(name=name)
    if not existing_schedule:
        schedule = Schedule(name=name, func='event.tasks.buy_and_place_orders_job',
                            schedule_type=Schedule.CRON,
                            cron='0 15 * * 1-5', repeats=-1)
        schedule.save()

    name = "Check orders and transactions"
    existing_schedule = Schedule.objects.filter(name=name)
    if not existing_schedule:
        schedule = Schedule(name=name, func='event.tasks.check_transactions_and_orders_job',
                            schedule_type=Schedule.CRON,
                            cron='0 20 * * 1-5', repeats=-1)
        schedule.save()
