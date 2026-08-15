from django.contrib import messages
from django.contrib.auth import login
from django.conf import settings
from django.http import FileResponse, Http404
from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from apps.core.serializers import HealthStatusSerializer
from .forms import RegistrationForm


def home(request):
    return render(request, "index.html")


def service_worker(request):
    """Serve the worker at the site root so it can cache the whole app."""
    worker_path = settings.BASE_DIR / "static" / "service-worker.js"
    if not worker_path.exists():
        raise Http404("Service worker was not found")
    response = FileResponse(worker_path.open("rb"), content_type="application/javascript")
    response["Service-Worker-Allowed"] = "/"
    response["Cache-Control"] = "no-cache"
    return response


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


@extend_schema(responses=HealthStatusSerializer)
@api_view(["GET"])
def api_health(request):
    """Check that the Muftiyat API is available."""
    return Response({"status": "ok", "service": "Muftiyat API"})
