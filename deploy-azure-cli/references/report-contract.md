# Contrato de salida

## 1. Resumen ejecutivo

- Estado: `LISTO`, `LISTO CON CORRECCIONES` o `BLOQUEADO`.
- Entorno y alcance.
- Arquitectura detectada en una frase.
- Riesgos principales.
- Decisión solicitada al usuario.

## 2. Inventario con evidencia

| Componente | Ruta | Tecnología/versiones | Build | Inicio | Puerto | Estado/persistencia | Evidencia |
|---|---|---|---|---|---|---|---|

Añadir dependencias entre componentes y servicios externos.

## 3. Variables

| Variable | Componente | Obligatoria | Secreta | Build/runtime | Estado | Evidencia |
|---|---|---:|---:|---|---|---|

Nunca incluir valores secretos.

## 4. Hallazgos

Ordenar por severidad:

| Severidad | Hallazgo | Evidencia | Impacto | Corrección | Verificación |
|---|---|---|---|---|---|

Separar hechos de inferencias y desconocidos.

## 5. Opciones de Azure

| Componente | Opción recomendada | Alternativa | Motivo | Descarte/limitaciones | Costo relativo |
|---|---|---|---|---|---|

Incluir una matriz de decisión cuando haya varias opciones razonables. Confirmar que el artefacto puede desplegarse exclusivamente con `az`.

## 6. Arquitectura propuesta

Describir:

- exposición pública/privada;
- identidad y secretos;
- red y DNS;
- datos, almacenamiento y backups;
- escalado y disponibilidad;
- observabilidad;
- flujo entre componentes.

No agregar recursos sin requisito asociado.

## 7. Correcciones antes de desplegar

Listar en orden, con archivos afectados, riesgo, prueba y necesidad de aprobación. No aplicar cambios todavía durante la fase de evaluación.

## 8. Plan Azure CLI

Para cada paso:

1. propósito;
2. comando `az` individual;
3. placeholders;
4. resultado esperado;
5. comando `az` de verificación;
6. rollback cuando aplique.

No incluir scripts, Portal, `azd`, Bicep, Terraform, SWA CLI ni comandos encadenados.

## 9. Validación posterior

| Criterio | Método Azure CLI | Resultado esperado | Estado/evidencia |
|---|---|---|---|

Separar pruebas funcionales externas que Azure CLI no pueda demostrar.

## 10. Registro final

Documentar:

- suscripción, región, grupo y nombres no sensibles;
- recursos y URLs;
- comandos ejecutados;
- resultados y timestamps;
- migraciones;
- desviaciones aprobadas;
- rollback;
- pendientes y responsable.

Redactar IDs o datos si la política del proyecto lo exige y nunca documentar secretos.
