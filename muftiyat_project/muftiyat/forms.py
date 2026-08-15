from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


User = get_user_model()


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(label="Аты", max_length=150, required=True)
    last_name = forms.CharField(label="Фамилиясы", max_length=150, required=False)
    email = forms.EmailField(label="Электрондук почта", required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")
        labels = {
            "username": "Колдонуучу аты",
            "password1": "Сырсөз",
            "password2": "Сырсөздү кайталаңыз",
        }

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Бул электрондук почта менен аккаунт мурунтан бар.")
        return email
