from .views import ExpenseSummaryStatsView, IncomeSourcesSummaryStatsView
from django.urls import path


urlpatterns = [
    path('expense-category-data/', ExpenseSummaryStatsView.as_view(), name='expense_category_data'),
    path('income-category-data/', IncomeSourcesSummaryStatsView.as_view(), name='income_category_data'),
]
