from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView



class TransactionsDetails(APIView):
    """API Details."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):       
        transactions_urls = {
            "Loans": "'loans/'",
            "Payments": "payments/",
        }          
    
        return Response(transactions_urls)
