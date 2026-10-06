# Flujo de Corrección Urgente (Hotfix)

Este flujo proporciona un proceso rápido, de precisión quirúrgica y seguro para resolver incidencias críticas o bugs bloqueantes en producción o desarrollo sin romper la arquitectura ni introducir sobreingeniería.

---

## Fases del Hotfix

```text
1. Diagnóstico Aislado ──> 2. Reproducción Mínima ──> 3. Parche Quirúrgico Ponytail ──> 4. Prueba de Regresión ──> 5. Despliegue y Registro
```

---

### Fase 1: Diagnóstico Aislado
- Identificar el error exacto (stack trace, código HTTP, mensaje de excepción).
- Consultar `graphify query` para ubicar puntualmente la función o archivo responsable.
- Comprimir la salida de error con **Headroom** para analizarla sin quemar tokens.

### Fase 2: Reproducción Mínima
- Escribir una prueba unitaria o aserción mínima reproducible que falle demostrando la existencia del bug (*Red*).
- Si no es posible escribir un test automatizado de inmediato, registrar los pasos de reproducción manual determinista.

### Fase 3: Parche Quirúrgico Ponytail
- Aplicar la modificación de código más pequeña que resuelva la falla.
- **Prohibición de refactors durante el hotfix**: No cambiar variables adyacentes, no renombrar carpetas ni formatear archivos completos.

### Fase 4: Prueba de Regresión
- Ejecutar la prueba creada en la Fase 2 y confirmar que ahora pasa exitosamente (*Green*).
- Ejecutar la suite de pruebas del módulo para certificar que no existen efectos secundarios.

### Fase 5: Despliegue Seguro y Registro
- Notificar la corrección con `scripts/notificar_tarea.py`.
- Registrar la causa raíz y la solución en `claude-mem` y en el manifiesto del proyecto.
- Solicitar aprobación humana antes de desplegar el parche a producción.
