# Memoria y adaptadores opcionales

La memoria local es la fuente operativa por defecto: [flujo](flujo_memoria.md). Markdown y JSONL facilitan lectura y trazabilidad; no son un almacén de secretos. El cifrado legacy conserva compatibilidad y no protege las copias legibles.

Un proveedor de memoria externo puede añadirse mediante un adaptador específico si el usuario autoriza transferencia, cuenta y alcance. Confirmar herramientas, esquema, identidad de sesión y política de retención. No inferir aprobación por detectar un ejecutable ni inventar identidad. Registrar datos enviados y resultado cuando la operación ocurra.

Si falta el adaptador, continuar localmente cuando cumpla el objetivo. No afirmar sincronización ni recuperación externa. La portabilidad depende de un contrato de lectura/escritura y no del nombre de un proveedor.
