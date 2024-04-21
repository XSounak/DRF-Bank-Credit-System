from django.urls import path
from .views import CheckEligibilityView, CreateLoanView

urlpatterns = [
    path('check-eligibility/', CheckEligibilityView.as_view(), name='check_eligibility'),
    path('create-loan/', CreateLoanView.as_view(), name='create_loan'),
    path('check-eligibility/<int:customer_id>/', CheckEligibilityView.as_view(), name='CheckEligibilityView')
]
