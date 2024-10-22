from typing import Any
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Transaction
from .forms import DepositForm, WithdrawForm, LoadRequestForm
from .constants import DEPOSITE, WITHDRAWAL, LOAN_PAID, LOAN
from django.contrib import messages
from django.http import HttpResponse
import datetime
from django.db import Sum


class TransactionCreateMixin(CreateView, LoginRequiredMixin):
    template_name = ""
    model = Transaction
    title = ""
    success_url = ""

    def get_form_kwargs(self) -> dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs.update({"account": self.request.user.account})
        return kwargs

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({"title": self.title})
        return context


class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm
    title = "Deposit"

    def get_initial(self):
        initial = {"transaction_type": DEPOSITE}
        return super().get_initial()

    def form_valid(self, form):
        amount = form.cleaned_data.get("amount")
        account = self.request.user.account
        account.balance += amount
        account.save(update_fields=["balance"])
        messages.success(f"{amount} was deposited to your account successfully")
        return super().form_valid(form)


class WithdrawMoneyView(TransactionCreateMixin):
    form_class = WithdrawForm
    title = "Withdraw"

    def get_initial(self):
        initial = {"transaction_type": WITHDRAWAL}
        return super().get_initial()

    def form_valid(self, form):
        amount = form.cleaned_data.get("amount")
        account = self.request.user.account
        account.balance += amount
        account.save(update_fields=["balance"])
        messages.success(f"Successfully withdrawn {amount} from your account")
        return super().form_valid(form)


class LoanRequestView(TransactionCreateMixin):
    form_class = LoadRequestForm
    title = "Load Request"

    def get_initial(self):
        initial = {"transaction_type": LOAN}
        return super().get_initial()

    def form_valid(self, form):
        amount = form.cleaned_data.get("amount")
        current_loan_count = Transaction.objects.filter(
            account=self.request.user.account, transaction_type=LOAN, loan_approve=True
        ).count()

        if current_loan_count >= 3:
            return HttpResponse("You have crossed your limits")
        messages.success(f"Your Loan request {amount} has been sent manager")
        return super().form_valid(form)

    def get_queryset(self):
        queryset = super().get_queryset().filter(account=self.request.user.account)

        start_date_str = self.request.GET.get("start_date")
        end_date_str = self.request.GET.get("end_date")

        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

            self.balance = Transaction.objects.filter(
                timestamp_date_gte=start_date, times_date_Ite=end_date
            ).aggregate(Sum("amount"))["amount_sum"]

        else:
            self.balance = self.request.user.account.balance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"account": self.request.user.account})
        return context


class PayLoanView(LoginRequiredMixin, View):
    def get(self, request, loan_id):
        loan = get_object_or_404(Transaction, id=loan_id)

        if loan.loan_approve:
            user_account = loan.account
            if loan.amount < user_account.balance:
                user_account.balance -= loan.amount
                loan.balance_after_transaction = user_account.balance
                user_account.save()
                loan.transaction_type = LOAN_PAID
                loan.save()
                return redirect()
            else:
                messages.warning(
                    self.request, "Loan amount is greater then available balance"
                )
                return redirect()


class LoanListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = ""
    context_object_name = ""

    def get_queryset(self):
        user_account = self.request.user.account
        querySet = Transaction.objects.filter(
            account=user_account, transaction_type=LOAN
        )
        return querySet
