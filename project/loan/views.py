from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Loan
from customer.models import Customer
from datetime import datetime

class CheckEligibilityView(APIView):
    
    def calculate_monthly_installment(self, loan_amount, interest_rate, tenure):
        r = interest_rate / 12 / 100
        n = tenure * 12
        monthly_installment = loan_amount * r * (pow(1 + r, n)) / (pow(1 + r, n) - 1)
        return round(monthly_installment, 2)

    def post(self, request, *args, **kwargs):
        try:
            customer_id = request.data['customer_id']
            loan_amount = request.data['loan_amount']
            interest_rate = request.data['interest_rate']
            tenure = request.data['tenure']

            customer = Customer.objects.get(id=customer_id)
            current_year = datetime.now().year
            past_loans = Loan.objects.filter(customer=customer, start_date__year=current_year)
            current_year_loans = past_loans.filter(end_date__year=current_year)

            
            current_emi = sum(loan.monthly_installment for loan in current_year_loans)

            approval = False

            credit_rating = 0

    
            if all(loan.paid_on_time for loan in past_loans):
                credit_rating += 10

            credit_rating += min(len(past_loans) // 2, 20)

            credit_rating += min(len(current_year_loans), 20)

            approved_volume = sum(loan.approved_amount for loan in past_loans)
            if approved_volume > customer.approved_limit:
                credit_rating = 0

           
            if sum(loan.approved_amount for loan in current_year_loans) > customer.approved_limit:
                credit_rating = 0

            if credit_rating > 50:
                approval = True
            elif 50 > credit_rating > 30 and interest_rate > 12:
                approval = True
            elif 30 > credit_rating > 10 and interest_rate > 16:
                approval = True
            elif 10 > credit_rating or current_emi > 0.5 * customer.monthly_income:
                approval = False

            
            corrected_interest_rate = min(interest_rate, 16)

            
            loan_amount = float(loan_amount) 
            monthly_installment = self.calculate_monthly_installment(loan_amount, corrected_interest_rate, tenure)

            response_data = {
                "customer_id": customer_id,
                "approval": approval,
                "interest_rate": interest_rate,
                "corrected_interest_rate": corrected_interest_rate,
                "tenure": tenure,
                "monthly_installment": monthly_installment,
                "credit_rating": credit_rating
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except KeyError as e:
            return Response({"error": f"KeyError: {e}"}, status=status.HTTP_400_BAD_REQUEST)

        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, *args, **kwargs):
        try:
            customer_id = self.kwargs['customer_id'] 
            customer = Customer.objects.get(id=customer_id)
            approval = False
            interest_rate = 10.0
            corrected_interest_rate = 10.0
            tenure = 12
            monthly_installment = 500.0

            response_data = {
                "customer_id": customer_id,
                "approval": approval,
                "interest_rate": interest_rate,
                "corrected_interest_rate": corrected_interest_rate,
                "tenure": tenure,
                "monthly_installment": monthly_installment,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except KeyError as e:
            return Response({"error": f"KeyError: {e}"}, status=status.HTTP_400_BAD_REQUEST)

        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

class CreateLoanView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            loan_id = request.data['loan_id']
            customer_id = request.data['customer_id']
            loan_approved = request.data['loan_approved']
            message = request.data['message']
            monthly_installment = request.data['monthly_installment']

            response_data = {
                "loan_id": loan_id,
                "customer_id": customer_id,
                "loan_approved": loan_approved,
                "message": message,
                "monthly_installment": monthly_installment,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except KeyError as e:
            return Response({"error": f"KeyError: {e}"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        try:
            customer_id = request.data['customer_id']
            loan_amount = request.data['loan_amount']
            interest_rate = request.data['interest_rate']
            tenure = request.data['tenure']

            customer = Customer.objects.get(id=customer_id)

            loan_approved = True  # Replace with your actual approval logic

            if loan_approved:
                new_loan = Loan.objects.create(
                    customer=customer,
                    loan_amount=loan_amount,
                    interest_rate=interest_rate,
                    tenure=tenure,
                    monthly_installment=self.calculate_monthly_installment(loan_amount, interest_rate, tenure)
                )

                # Prepare the response data
                response_data = {
                    "loan_id": new_loan.id,
                    "customer_id": customer_id,
                    "loan_approved": loan_approved,
                    "message": "Loan approved!",
                    "monthly_installment": new_loan.monthly_installment
                }
            else:
                # If the loan is not approved, provide an appropriate message
                response_data = {
                    "loan_id": None,
                    "customer_id": customer_id,
                    "loan_approved": False,
                    "message": "Loan not approved.",
                    "monthly_installment": 0.0
                }

            return Response(response_data, status=status.HTTP_200_OK)

        except KeyError as e:
            return Response({"error": f"KeyError: {e}"}, status=status.HTTP_400_BAD_REQUEST)

        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def calculate_monthly_installment(self, loan_amount, interest_rate, tenure):
        r = interest_rate / 12 / 100
        n = tenure * 12
        monthly_installment = loan_amount * r * (pow(1 + r, n)) / (pow(1 + r, n) - 1)
        return round(monthly_installment, 2)
