\# Auditoría de Seguridad ASVS Nivel 2 - DentalSecureLab



\## 1. Objetivo y Alcance

Documentar las verificaciones y el blindaje del módulo de Autenticación y Login del sistema DentalSecureLab, cumpliendo con los estándares de seguridad OWASP ASVS Nivel 2 y la directiva PRO-DES-06.



\## 2. Metodología TDD

Se aplicó desarrollo guiado por pruebas (TDD):

\- \*\*Red:\*\* Se verificó la carencia inicial de un formulario web estructurado con protección CSRF en el login.

\- \*\*Green:\*\* Se implementó la plantilla con campos seguros, token CSRF y configuraciones de cookies.

\- \*\*Refactor:\*\* Se validó la ejecución exitosa de la suite de pruebas unitarias.



\## 3. Controles Evaluados y Trazabilidad



\### Control 5.1: Autenticación y Protección de Credenciales

\- \*\*ASVS Requisito:\*\* Verificación de controles de autenticación robusta y protección contra falsificación de peticiones en sitios cruzados (CSRF).

\- \*\*Vulnerabilidad:\*\* Falta de formulario HTML estructurado y token CSRF visible en la plantilla de inicio de sesión.

\- \*\*Archivo afectado:\*\* `templates/users/login.html` y `config/settings.py`.

\- \*\*Función / Componente:\*\* `login\_view` y políticas de cookies de sesión (`SESSION\_COOKIE\_HTTPONLY`, `SESSION\_COOKIE\_SAMESITE`, `CSRF\_COOKIE\_SAMESITE`).

\- \*\*Cambio realizado:\*\* Se incorporaron las etiquetas `<form>`, los campos de entrada requeridos y la directiva `{% csrf\_token %}` en el HTML, junto con el endurecimiento de cookies en `settings.py`.

\- \*\*Test asociado:\*\* `test\_pagina\_login\_existe` y pruebas de ejecución del cliente Django.

\- \*\*Evidencia:\*\* Captura de pantalla `03\_pruebas\_despues\_del\_cambio.png` mostrando las 8 pruebas en estado `OK`.

\- \*\*Commit:\*\* Registro formal en la rama `security/login-hardening`.



\## 4. Conclusión Provisional

El módulo de login cuenta con la estructura base blindada, cookies seguras y validación de pruebas unitarias en verde.

