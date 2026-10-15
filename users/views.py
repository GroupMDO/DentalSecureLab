from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.utils.http import url_has_allowed_host_and_scheme

def login_view(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            
            # Sanitización de redirección 'next' (Prevención de Open Redirect)
            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url and url_has_allowed_host_and_scheme(url=next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect('dashboard')
        else:
            error = "Usuario o contraseña incorrectos"

    return render(
        request,
        "users/login.html",
        {"error": error}
    )

def logout_view(request):
    logout(request)
    return redirect('login')