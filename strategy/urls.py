from django.urls import path

from manage import RUN_MODE
from strategy.models import StockStrategy, StrategyCriteria
from strategy.views import StrategyListView

urlpatterns = [
    path('strategy-list/', StrategyListView.as_view(), name='strategy-list'),

]

if RUN_MODE:
    # First Strategy
    stock_strategy = StockStrategy(name="First Strategy", description="Test strategy")
    existing_stock_strategy = StockStrategy.objects.filter(name=stock_strategy.name)
    if not existing_stock_strategy:
        new_existing_stock_strategy = StockStrategy.objects.create(name=stock_strategy.name, description=stock_strategy.description)
        new_existing_stock_strategy.save()

        critera_1 = StrategyCriteria.objects.create(stock_strategy=new_existing_stock_strategy,
                                                    data_name="CHANGE_PERCENT",
                                                    value_direction="ABOVE",
                                                    value_selection="0"
                                                    )
        critera_1.save()
