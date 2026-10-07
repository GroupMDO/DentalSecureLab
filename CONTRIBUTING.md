# Guía de Contribución y Control de Versiones (INS-GIT-01)
Proyecto: DentalSecureLab | Proceso base: PRO-DES-02 Controlar versiones

## 1. Nomenclatura de Ramas Obligatoria
- Funcionalidades: feature/<modulo>-<descripcion> (ej. feature/auth-login)
- Seguridad ASVS: security/sec-<num>-<descripcion> (ej. security/sec-01-auditlog)
- Corrección de bugs: fix/<ticket>-<descripcion> (ej. fix/tk-04-session)

## 2. Formato Estricto de Commits
ASVS → vulnerabilidad → archivo → clase/función → cambio → test → evidencia → commit

## 3. Requisitos para Pull Request
- Pruebas al 100% en PASS (python manage.py test).
- Reporte de pip-audit con 0 CVEs.
- Prohibido incluir archivos .env o credenciales.