
# Django imports
from django.urls import path

# Transactions app imports
from transactions import views

urlpatterns = [
    # Transactions endpoints overview
    path('', 
         views.TransactionsOverview.as_view(), 
         name='transactions_overview'),
    
    # Transactions endpoints
    path('loans/', 
         views.LoansList.as_view(), 
         name='loans_list'),
    path('loans/<int:pk>/', 
         views.LoanDetail.as_view(), 
         name='loan_detail'),
    path('loans/<int:pk>/payments/', 
         views.PaymentsPerLoan.as_view(), 
         name='payments_per_loan'),
    path('payments/', 
         views.PaymentsList.as_view(), 
         name='payments_list'),
    path('payments/<int:pk>/', 
         views.PaymentDetail.as_view(), 
         name='payment_detail')
]