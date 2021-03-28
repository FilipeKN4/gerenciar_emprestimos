
# Django imports
from django.urls import path

# Transactions app imports
from transactions import views

urlpatterns = [
    # Transactions Details endpoint
    path('', views.TransactionsDetails.as_view(), name='transactions_details'),
]