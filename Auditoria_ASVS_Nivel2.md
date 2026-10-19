\# Auditoría de Seguridad Web — OWASP ASVS Nivel 2



\## 1. Identificación del trabajo



\- \*\*Proyecto:\*\* DentalSecureLab

\- \*\*Instrucción:\*\* PRO-DES-06

\- \*\*Ticket relacionado:\*\* TK-2026-004 — Módulo de autenticación y login con roles

\- \*\*Responsabilidad:\*\* Seguridad Web / DevSecOps

\- \*\*Rama de trabajo:\*\* `security/login-hardening`

\- \*\*Estándar de referencia:\*\* OWASP Application Security Verification Standard (ASVS), Nivel 2

\- \*\*Fecha de inicio:\*\* 10 de octubre de 2026

\- \*\*Estado:\*\* En progreso



\## 2. Objetivo



Revisar y reforzar la seguridad del módulo de autenticación, con especial atención a la protección de credenciales, sesiones, intentos fallidos de inicio de sesión y autorización por roles.



\## 3. Alcance



\- Inicio de sesión con credenciales válidas e inválidas.

\- Protección y configuración de sesiones y cookies.

\- Revisión de intentos repetidos de autenticación fallidos.

\- Control de acceso para los roles Administrador, Operador y Soporte.

\- Restricción de acceso a usuarios no autenticados.

\- Pruebas automatizadas, pruebas de regresión y registro de evidencias.



\## 4. Metodología TDD



1\. \*\*RED:\*\* ejecutar una prueba y registrar el resultado real antes del cambio.

2\. \*\*GREEN:\*\* implementar el cambio mínimo necesario y repetir la prueba.

3\. \*\*REFACTOR:\*\* revisar el cambio y ejecutar las pruebas de regresión.



No se registrarán resultados ni evidencias que no se hayan obtenido realmente.



\## 5. Controles en revisión



\### 5.1 Autenticación y protección del login



\- \*\*Referencia ASVS específica:\*\* pendiente de verificar.

\- \*\*Riesgo:\*\* acceso no autorizado por debilidades en la autenticación.

\- \*\*Archivos relacionados:\*\* `users/views.py`, `users/tests.py`, `templates/users/login.html`.

\- \*\*Función principal identificada:\*\* `login\_view`.

\- \*\*Estado inicial:\*\* pendiente de validar mediante pruebas.

\- \*\*RED:\*\* pendiente.

\- \*\*GREEN:\*\* pendiente.

\- \*\*Regresión:\*\* pendiente.

\- \*\*Evidencias:\*\* pendientes.

\- \*\*Commit:\*\* pendiente.



\### 5.2 Sesiones y cookies



\- \*\*Referencia ASVS específica:\*\* pendiente de verificar.

\- \*\*Riesgo:\*\* exposición o uso indebido de sesiones.

\- \*\*Archivo relacionado:\*\* `config/settings.py`.

\- \*\*Observación inicial:\*\* se identificaron los middleware de sesiones, protección CSRF y autenticación. La búsqueda inicial no encontró configuraciones explícitas de seguridad para cookies y sesiones.

\- \*\*Resultado de pruebas:\*\* pendiente.

\- \*\*Evidencias y commit:\*\* pendientes.



\### 5.3 Intentos fallidos de inicio de sesión



\- \*\*Referencia ASVS específica:\*\* pendiente de verificar.

\- \*\*Riesgo:\*\* intentos repetidos de adivinar contraseñas.

\- \*\*Observación inicial:\*\* se identificó un PR relacionado con el bloqueo temporal tras cinco intentos fallidos. Se revisará para evitar duplicar cambios.

\- \*\*Resultado de pruebas:\*\* pendiente.

\- \*\*Evidencias y commit:\*\* pendientes.



\### 5.4 Autorización por roles



\- \*\*Referencia ASVS específica:\*\* pendiente de verificar.

\- \*\*Riesgo:\*\* acceso a funciones sin los permisos correspondientes.

\- \*\*Archivos relacionados:\*\* `records/views.py`, `users/tests.py`.

\- \*\*Observación inicial:\*\* se identificó una restricción para el rol Soporte en vistas de expedientes. Queda pendiente validar el acceso anónimo y los permisos de cada operación.

\- \*\*Roles por validar:\*\* Administrador, Operador y Soporte.

\- \*\*Resultado de pruebas:\*\* pendiente.

\- \*\*Evidencias y commit:\*\* pendientes.



\## 6. Resumen de pruebas



| Prueba | Estado |

|---|---|

| Login válido e inválido | Pendiente de ejecutar |

| Acceso al dashboard sin autenticación | Pendiente de ejecutar |

| Configuración de sesiones y cookies | Pendiente de validar |

| Bloqueo tras cinco intentos fallidos | Pendiente de revisar y probar |

| Permisos por rol | Pendiente de validar |

| Acceso anónimo a operaciones protegidas | Pendiente de ejecutar |

| Suite de regresión | Pendiente de ejecutar |



\## 7. Evidencias



Se agregarán capturas reales de las pruebas iniciales, los cambios de seguridad, las pruebas aprobadas y la regresión. Las capturas no deberán mostrar contraseñas, tokens ni otros datos sensibles.



\## 8. Trazabilidad



Para cada control se registrará la siguiente información:



\*\*ASVS → riesgo o vulnerabilidad → archivo → función → cambio → prueba → evidencia → commit.\*\*



\## 9. Conclusión



La auditoría se encuentra en fase inicial. La presencia de middleware de seguridad no demuestra por sí sola que todos los controles estén correctamente implementados. La conclusión final se completará después de ejecutar las pruebas, revisar los controles, realizar los cambios necesarios y registrar la evidencia.





