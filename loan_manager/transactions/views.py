# Django imports
from django.http import Http404
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Transactions app imports
from transactions.api.serializers import LoanSerializer, PaymentSerializer
from transactions.models import Loan, Payment


class TransactionsOverview(APIView):
    """Transactions overview."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        loan_urls = {
            "list": "loans/",
            "detail": "loans/<int:pk>/",
            "payments_per_loan": "loans/<int:pk>/payments/"
        }
        
        payment_urls = {
            "list": "payments/",
            "detail": "payments/<int:pk>/",
        }
          
        transactions_urls = {
            "loans": loan_urls,
            "payments":payment_urls,
        }          
    
        return Response(transactions_urls)
    

class LoansList(APIView):
    """List all loans or create a new loan."""
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        if request.user.is_admin:
            loans = Loan.objects.all()
        else:
            loans = Loan.objects.filter(user_account=request.user)
        serializer = LoanSerializer(loans, 
                                    context={'request': request}, 
                                    many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = LoanSerializer(data=request.data, 
                                    context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoanDetail(APIView):
    """Retrieve, update or delete a loan instance."""
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return Loan.objects.get(pk=pk)
        except Loan.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        loan = self.get_object(pk)
        if loan.user_account != request.user and not request.user.is_admin:
            return Response(
                {'detail': "You don't have permission to view this content."}
            )
        
        serializer = LoanSerializer(loan, 
                                    context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        loan = self.get_object(pk)
        if loan.user_account != request.user:
            return Response(
                {'detail': "You don't have permission to edit this content."}
            )
        
        serializer = LoanSerializer(loan, 
                                    data=request.data, 
                                    context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        loan = self.get_object(pk)
        if loan.user_account != request.user:
            return Response(
                {'detail': "You don't have permission to delete this content."}
            )
        
        loan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PaymentsPerLoan(APIView):
    """List all payments of a loan."""
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk, format=None):
        loan = Loan.objects.get(pk=pk)
        if loan.user_account != request.user and not request.user.is_admin:
            return Response(
                {'detail': "You don't have permission to view this content."}
            )
        payments = Payment.objects.filter(loan=loan)
        serializer = PaymentSerializer(payments, 
                                       context={'request': request}, 
                                       many=True)
        return Response(serializer.data)
    
    
class PaymentsList(APIView):
    """List all payments or create a new payment."""
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        if request.user.is_admin:
            payments = Payment.objects.all()
        else:
            payments = Payment.objects.filter(loan__user_account=request.user)
        serializer = PaymentSerializer(payments, 
                                       context={'request': request}, 
                                       many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PaymentSerializer(data=request.data, 
                                       context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentDetail(APIView):
    """Retrieve, update or delete a payment instance."""
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return Payment.objects.get(pk=pk)
        except Payment.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        payment = self.get_object(pk)
        if payment.loan.user_account != request.user and not request.user.is_admin:
            return Response(
                {'detail': "You don't have permission to view this content."}
            )
        
        serializer = PaymentSerializer(payment, 
                                    context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        payment = self.get_object(pk)
        if payment.loan.user_account != request.user:
            return Response(
                {'detail': "You don't have permission to edit this content."}
            )
        
        serializer = PaymentSerializer(payment, 
                                    data=request.data, 
                                    context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        payment = self.get_object(pk)
        if payment.loan.user_account != request.user:
            return Response(
                {'detail': "You don't have permission to delete this content."}
            )
    
        payment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)