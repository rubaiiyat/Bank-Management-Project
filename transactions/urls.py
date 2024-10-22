from django.urls import path
from .views import (
    DepositMoneyView,
    WithdrawMoneyView,
    TransactionReportView,
    LoanRequestView,
    PayLoanView,
    LoanListView,
)

urlpatterns = [
    path("deposit/", DepositMoneyView.as_view(), name="deposit"),
    path("report/", TransactionReportView.as_view(), name="transaction_report"),
    path("withdraw/", WithdrawMoneyView.as_view(), name="withdraw"),
    path("loan_request/", LoanRequestView.as_view(), name="loan_request"),
    path("loans/<int:loan_id", PayLoanView.as_view(), name="loans"),
    path("loans/", LoanListView.as_view(), name="loan_list"),
]
