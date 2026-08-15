from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .forms import RegistrationForm


def home(request):
    return render(request, "index.html")


def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Каттоо ийгиликтүү аяктады. Кош келиңиз!")
            return redirect("home")
    else:
        form = RegistrationForm()
    return render(request, "register.html", {"form": form})


@api_view(["GET"])
def api_health(request):
    """Check that the Muftiyat API is available."""
    return Response({"status": "ok", "service": "Muftiyat API"})
