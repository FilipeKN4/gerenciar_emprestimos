# Django imports
from django.http import HttpResponse, Http404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Transactions app imports
from transactions.api.serializers import LoanSerializer, PaymentSerializer
from transactions.models import Loan, Payment


class TransactionsOverview(APIView):
    """Transactions overview."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):       
        transactions_urls = {
            "Loans": "'loans/'",
            "Payments": "payments/",
        }          
    
        return Response(transactions_urls)
    

class LoansList(APIView):
    """List all loans or create a new loan from a user."""
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        loans = Loan.objects.all()
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = LoanSerializer(data=request.data)
        if serializer.is_valid():
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
        serializer = LoanSerializer(loan)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        loan = self.get_object(pk)
        serializer = LoanSerializer(loan, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        loan = self.get_object(pk)
        loan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
