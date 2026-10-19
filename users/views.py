
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.utils.http import url_has_allowed_host_and_scheme


def login_view(request):
    error = None

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        next_url = request.POST.get("next", "")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:
            login(request, user)

            if next_url and url_has_allowed_host_and_scheme(
                url=next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)

            return redirect("dashboard")

        error = "Usuario o contraseña incorrectos"

    next_url = (
        request.POST.get("next", "")
        if request.method == "POST"
        else request.GET.get("next", "")
    )

    if not url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        next_url = ""

    return render(
        request,
        "users/login.html",
        {
            "error": error,
            "next": next_url,
        },
    )
