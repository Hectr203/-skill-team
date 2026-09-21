# Investigación continua de seguridad

Esta agencia mantiene un catálogo de opciones, pero no instala herramientas
externas automáticamente. En cada revisión trimestral el Director registra
repositorio, mantenedor, licencia SPDX, fecha de actualización, alcance,
permisos, datos observados, sandbox, falsos positivos conocidos y alternativa.

| Área | Opciones a evaluar | Evidencia mínima antes de adoptar |
|---|---|---|
| SAST | Semgrep, Sonar, ESLint Security | regla reproducible, licencia, salida sin secretos |
| Secretos | Gitleaks, TruffleHog, detect-secrets | fixture local, rotación sin imprimir valores |
| SCA/SBOM | OSV-Scanner, npm audit, Trivy | lockfile, CVE reproducible, excepción fechada |
| Contenedores/IaC | Trivy, Hadolint, Checkov | Docker/Kubernetes/Terraform en sandbox |
| API/DAST | OpenAPI validators, ZAP en fixture | contrato, cabeceras y límites; nunca producción |

La adopción requiere aprobación humana si instala dependencias, accede a red,
lee credenciales o escribe fuera del directorio de auditoría. Los agentes de
auditoría sólo producen evidencia, `needs_validation` o planes; no corrigen el
código. Cada ejecución conserva un ledger de cobertura y un verificador distinto
al descubridor.
