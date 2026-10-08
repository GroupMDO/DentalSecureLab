from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.utils import timezone


MAX_INTENTOS = 5
TIEMPO_BLOQUEO = 300  # 5 minutos


class LoginSeguroView(LoginView):
    template_name = 'registration/login.html'

    def post(self, request, *args, **kwargs):
        bloqueado_hasta = request.session.get('bloqueado_hasta')

        # Comprobar si existe un bloqueo activo
        if bloqueado_hasta:
            fecha_bloqueo = timezone.datetime.fromisoformat(bloqueado_hasta)

            if timezone.now() < fecha_bloqueo:
                messages.error(
                    request,
                    'Inicio de sesión bloqueado temporalmente. Intenta nuevamente en 5 minutos.'
                )

                # Mostrar nuevamente el formulario sin procesar el login
                return self.get(request, *args, **kwargs)

            # El tiempo de bloqueo ya terminó
            request.session['intentos_login'] = 0
            request.session.pop('bloqueado_hasta', None)

        return super().post(request, *args, **kwargs)

    def form_invalid(self, form):
        intentos = self.request.session.get('intentos_login', 0) + 1
        self.request.session['intentos_login'] = intentos

        if intentos >= MAX_INTENTOS:
            bloqueado_hasta = timezone.now() + timezone.timedelta(
                seconds=TIEMPO_BLOQUEO
            )

            self.request.session['bloqueado_hasta'] = bloqueado_hasta.isoformat()

            messages.error(
                self.request,
                'Se alcanzaron 5 intentos fallidos. Inicio de sesión bloqueado durante 5 minutos.'
            )

        return super().form_invalid(form)

    def form_valid(self, form):
        self.request.session['intentos_login'] = 0
        self.request.session.pop('bloqueado_hasta', None)

        return super().form_valid(form)
    
    