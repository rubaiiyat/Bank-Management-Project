from typing import Any
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .constants import ACCOUNT_TYPE, GENDER_TYPE
from .models import UserBankAccount, userAddress


class userRegistrationForm(UserCreationForm):
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE, required=True)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    gender = forms.ChoiceField(choices=GENDER_TYPE, required=True)
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
            "street_address",
            "city",
            "postal_code",
            "country",
        ]

    def save(self, commit=True):
        acc_user = super().save(commit=True)

        if commit == True:
            acc_user.save()
            account_type = self.cleaned_data.get("account_type")
            birth_date = self.cleaned_data.get("birth_date")
            gender = self.cleaned_data.get("gender")
            street_address = self.cleaned_data.get("street_address")
            city = self.cleaned_data.get("city")
            postal_code = self.cleaned_data.get("postal_code")
            country = self.cleaned_data.get("country")

            userAddress.objects.create(
                user=acc_user,
                street_address=street_address,
                city=city,
                postal_code=postal_code,
                country=country,
            )

            UserBankAccount.objects.create(
                user=acc_user,
                account_type=account_type,
                account_no=100000 + acc_user.id,
                birth_date=birth_date,
                gender=gender,
            )
        return acc_user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    "class": (
                        "appearance-none block w-full bg-gray-900 text-gray-300 "
                        "border border-gray-600 rounded-lg py-3 px-4 leading-tight "
                        "focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 "
                        "hover:border-blue-400 transition duration-200 ease-in-out"
                    ),
                    "placeholder": f"Enter your {field.replace('_', ' ').capitalize()}",
                }
            )


class userUpdateForm(forms.ModelForm):
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE, required=True)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    gender = forms.ChoiceField(choices=GENDER_TYPE, required=True)
    street_address = forms.CharField(max_length=50)
    city = forms.CharField(max_length=50)
    postal_code = forms.IntegerField()
    country = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    "class": (
                        "appearance-none block w-full bg-gray-900 text-gray-300 "
                        "border border-gray-600 rounded-lg py-3 px-4 leading-tight "
                        "focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 "
                        "hover:border-blue-400 transition duration-200 ease-in-out"
                    ),
                    "placeholder": f"Enter your {field.replace('_', ' ').capitalize()}",
                }
            )

        if self.instance:
            try:
                user_account = self.instance.account
                user_address = self.instance.address
            except:
                user_account = None
                user_address = None

            if user_account:
                self.fields["account_type"].initial = user_account.account_type
                self.fields["gender"].initial = user_account.gender
                self.fields["birth_date"].initial = user_account.birth_date
                self.fields["street_address"].initial = user_address.street_address
                self.fields["city"].initial = user_address.city
                self.fields["postal_code"].initial = user_address.postal_code
                self.fields["country"].initial = user_address.country

    def save(self, commit=True):
        user = super().save(commit=True)

        if commit == True:
            user.save()
            user_account, created = UserBankAccount.objects.get_or_create(user=user)
            user_address, created = userAddress.objects.get_or_create(user=user)

            user_account.account_type = self.cleaned_data.get("account_type")
            user_account.birth_date = self.cleaned_data.get("birth_date")
            user_account.gender = self.cleaned_data.get("gender")
            user_account.save()

            user_address.street_address = self.cleaned_data.get("street_address")
            user_address.city = self.cleaned_data.get("city")
            user_address.postal_code = self.cleaned_data.get("postal_code")
            user_address.country = self.cleaned_data.get("country")
            user_address.save()

        return user
