from django.contrib.auth import authenticate, login
from django.core.cache import cache
from django.shortcuts import render, redirect
from django.utils.http import url_has_allowed_host_and_scheme

MAX_FAILED_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION_SECONDS = 900  # 15 minutos


def login_view(request):
    error = None

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        next_url = request.POST.get("next", "")

        cache_key = f"login_attempts_{username.lower()}"
        intentos_fallidos = cache.get(cache_key, 0)

        if username and intentos_fallidos >= MAX_FAILED_LOGIN_ATTEMPTS:
            error = "Cuenta bloqueada temporalmente por acumular 5 intentos fallidos. Intente de nuevo en 15 minutos."
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
                status=403,
            )

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:
            if username:
                cache.delete(cache_key)

            login(request, user)

            if next_url and url_has_allowed_host_and_scheme(
                url=next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)

            return redirect("dashboard")

        if username:
            nuevos_intentos = intentos_fallidos + 1
            cache.set(cache_key, nuevos_intentos, timeout=LOCKOUT_DURATION_SECONDS)
            if nuevos_intentos >= MAX_FAILED_LOGIN_ATTEMPTS:
                error = "Cuenta bloqueada temporalmente por acumular 5 intentos fallidos. Intente de nuevo en 15 minutos."
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
                    status=403,
                )

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

