from typing import Any
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .constants import ACCOUNT_TYPE, GENDER_TYPE
from .models import UserBankAccount, userAddress


class userRegistrationForm(UserCreationForm):
    account_type = forms.CharField(max_length=20, choices=ACCOUNT_TYPE)
    birth_date = forms.DateField(null=True, blank=True)
    gender = forms.CharField(max_length=20, choices=GENDER_TYPE)
    street_address = forms.CharField(max_length=50)
    city = forms.CharField(max_length=50)
    postal_code = forms.IntegerField()
    country = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "account_type",
            "birth_date",
            "gender",
            "street",
            "city",
            "postal_code",
            "country",
        ]

    def save(self, commit=True):
        acc_user = super().save(commit=False)

        if commit == True:
            acc_user.save()
            account_type = self.cleaned_data.get("account_type")
            birth_date = self.cleaned_data.get("birth_date")
            gender = self.cleaned_data.get("gendere")
            street_address = self.cleaned_data.get("street_address")
            city = self.cleaned_data.get("city")
            postal_code = self.cleaned_data.get("postal_code")
            country = self.cleaned_data.get("country")

            userAddress.objects.create(
                user=acc_user,
                street=street_address,
                city=city,
                postal_code=postal_code,
                country=country,
            )

            UserBankAccount.objects.create(
                user=acc_user,
                account_type=10000000+acc_user.id
                birth_date=birth_date,
                gender=gender,
            )
        return acc_user