# Especificación de Diseño: Optimización Jerárquica y Gestión de Memoria para LLMs

- **Fecha:** 2026-10-17 (Revisada y Corregida)
- **Área:** Motor de Contexto y Persistencia de Memoria de Proyecto
- **Ubicación:** `Agencia_Principal/scripts/memoria_proyecto.py`, `Agencia_Principal/scripts/arranque.py`, `Agencia_Principal/scripts/cierre.py`, `Agencia_Principal/scripts/agencia.py`

---

## 1. Contexto, Objetivos y Diagnóstico de Contradicciones

### 1.1 Problema Identificado
En `Agencia_Principal`, los proyectos registran su actividad en `contexts/projects/<id>/memoria.md` y en `.memoria/timeline.jsonl`. Históricamente, `memoria.md` acumulaba sesiones de forma indefinida y plana. Al ejecutar `arranque.py --prime`, se inyectaba el documento entero en el prompt de contexto ("Context Primer"). A medida que un proyecto crece, esto provoca:
1. **Saturación innecesaria de tokens:** Prompts de decenas de miles de tokens que encarecen la inferencia y consumen presupuesto de ventana.
2. **Degradación de atención ("Lost in the Middle"):** El LLM diluye su foco entre decenas de tareas pasadas y concluidas, restando atención al estado activo y a las decisiones clave.
3. **Pérdida de contexto ante compactaciones ingenuas:** Eliminar sesiones pasadas sin consolidar pendientes abiertos ni verificar que el detalle existe en el historial causa amnesia operativa.

### 1.2 Corrección de Contradicciones y Supuestos de la Propuesta Original
La especificación inicial contenía contradicciones técnicas que deben corregirse formalmente:
1. **Falsa equivalencia en FinOps:** Comparar el prompt enfocado con la suma de archivos en disco inflaba artificialmente el porcentaje de ahorro. La métrica honesta debe comparar el prompt enfocado con un prompt de referencia completo equivalente sobre el mismo proyecto. El almacenamiento en disco se reporta por separado.
2. **La ventana deslizante no elimina por sí sola la pérdida de contexto:** Si un pendiente o regla técnica de la sesión 1 se compacta y desaparece de la ventana deslizante sin ser promovido al **Estado Activo**, el agente lo olvidará en la sesión 6. La información crítica debe mantenerse mientras siga vigente, sin importar su antigüedad.
3. **Riesgo de pérdida de datos por compactación ciega:** Proyectos legacy (como memorias anteriores a la activación de timeline) tienen detalle en Markdown que no está en `timeline.jsonl`. Truncar esas sesiones a una línea destruye información irreversiblemente. Se exige comprobar la presencia previa en el historial y archivar íntegramente antes de compactar.
4. **Fragilidad de regex:** Expresiones regulares simples fallaban al encontrar encabezados dentro de bloques de código Markdown o con variantes de formato. Se requiere un parser consciente de bloques de código y tolerante a formatos antiguos.
5. **Idempotencia y atomicidad transaccional:** La rotación y el cierre deben ser estrictamente idempotentes y transaccionales bajo un único bloqueo de archivo (`.lock`), garantizando que fallos intermedios no corrompan la memoria ni dupliquen hitos.

---

## 2. Arquitectura de Dos Capas

El sistema opera con dos capas independientes y complementarias:

```
┌────────────────────────────────────────────────────────────────────────┐
│  CAPA 1: HISTORIAL PERSISTENTE E INMUTABLE (Auditoría y Recuperación) │
│  - .memoria/timeline.jsonl (Registro append-only con IDs de evento)    │
│  - .memoria/cloudmem.jsonl (Compatibilidad y respaldo)                │
│  - adrs/ (Decisiones arquitectónicas completas)                        │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Generación / Sincronización
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│  CAPA 2: CONTEXTO DE TRABAJO (memoria.md & Context Engine)            │
│  - Sección 1: Estado Activo y Criterios Vigentes                       │
│  - Sección 2: Decisiones Técnicas y Reglas Vigentes                    │
│  - Sección 3: Sesiones Recientes (Ventana Deslizante: N sesiones)      │
│  - Sección 4: Hitos Anteriores (Bitácora compactada con referencias)   │
└────────────────────────────────────────────────────────────────────────┘
```

### 2.1 Estructura Formal de `memoria.md`
El archivo `memoria.md` se define como una vista estructurada, legible tanto por humanos como por LLMs, y totalmente reconstruible desde el timeline:

```markdown
# Memoria del Proyecto: <id>

- **ID de Proyecto:** `<id>`
- **Fecha de creación:** <ISO-8601>
- **Estado general:** <Activo/En progreso/Inicializado>

---

## 1. Estado Activo y Criterios Vigentes
- **Objetivo actual:** <Alcance del trabajo activo>
- **Hito/Sprint:** <Fase de ejecución>
- **Tarea en curso:** <Descripción o Ninguna>
- **Restricciones y bloqueos:** <Restricciones operativas o Ninguno>
- **Pendientes consolidados:**
  - [ ] <Pendiente 1>
  - [ ] <Pendiente 2>
- **Siguiente acción:** <Paso inmediato a ejecutar>

---

## 2. Decisiones Técnicas y ADRs
- `<ADR-XXX>`: <Título y síntesis de decisión> (Fuente: `adrs/ADR-XXX.md`)
- `<DEC-YYYYMMDD-N>`: <Regla técnica o decisión acordada>

---

## 3. Historial Reciente (Ventana Deslizante: Últimas N Sesiones)

### [2026-10-17T20:00:00+00:00] Sesión: <id_evento> | Agente: <Rol>
- **ID Evento:** `<id_evento>`
- **Tareas completadas:** <Detalle de tareas>
- **Archivos afectados:** `<ruta1>`, `<ruta2>`
- **Decisiones técnicas:** <Decisión o Ninguna>
- **Pendientes:** <Pendientes surgidos>
- **Riesgos:** <Riesgos detectados>

---

## 4. Hitos Anteriores (Bitácora Compactada)
- [<Fecha>] [<id_evento>] (<Agente>) <Resumen de tareas> (<N> archivos) — Ref: timeline#<id_evento>
```

---

## 3. Política de Selección de Contexto y Presupuesto

### 3.1 Presupuesto Configurable
La ventana de $N$ sesiones (por defecto 5) acota la cantidad de sesiones, pero no el tamaño de tokens. Se incorpora un presupuesto configurable (`presupuesto_tokens`, por defecto 4,000 tokens en memoria enfocada, parametrizable vía CLI o variable de entorno `AGENCIA_CONTEXT_BUDGET`).

### 3.2 Orden de Prioridad de Selección
Cuando el contenido compite por presupuesto, el motor selecciona en este orden estricto:
1. **Objetivo, alcance y restricciones de la tarea.**
2. **Estado activo y bloqueos (Sección 1).**
3. **Decisiones técnicas y ADRs vigentes (Sección 2).**
4. **Pendientes consolidados relacionados.**
5. **Sesiones recientes relevantes (Sección 3):** de la más reciente a la más antigua.
6. **Referencias históricas necesarias (Sección 4 o consulta puntual).**

### 3.3 Reglas de Compactación bajo Presupuesto
- Si la ventana de 5 sesiones excede el presupuesto, las sesiones más antiguas dentro de la ventana se compactan primero a un resumen con ID de evento antes de truncar.
- **Prohibido truncar en silencio:** Requisitos, identificadores de eventos, restricciones y advertencias críticas nunca se omiten. Si la Sección 1 por sí sola excede el límite, se emite una advertencia explícita en el informe FinOps.

### 3.4 Mecanismo de Recuperación Histórica Puntual
En lugar de forzar al LLM a cargar todo el historial, se proporciona recuperación selectiva por:
- ID de evento (`--evento <id>`).
- Tarea o palabra clave (`--query <texto>`).
- Archivo afectado (`--archivo <ruta>`).
- Rango de fechas (`--desde <iso>` / `--hasta <iso>`).

Disponible mediante `python3 scripts/agencia.py historia <proyecto> ...` y la función `recuperar_historia()`.

---

## 4. Concurrencia, Integridad y Recuperación ante Fallos

1. **Bloqueo Exclusivo de Transacción:** Toda la operación de lectura de estado, validación, anexado a `timeline.jsonl`, regeneración de `memoria.md` y actualización Fernet se ejecuta bajo un único contexto `bloqueo_proyecto` (`fcntl.flock(LOCK_EX)`).
2. **Orden Seguro de Escritura:**
   - Paso 1: Anexar evento completo con `fsync` a `.memoria/timeline.jsonl` (y `cloudmem.jsonl`).
   - Paso 2: Generar y escribir `memoria.md` mediante archivo temporal y reemplazo atómico (`os.replace`).
   - Paso 3: Actualizar `mem_palace.enc` atómicamente si cryptography está activo.
3. **Tolerancia a Corrupción en JSONL:** El lector de timeline descarta líneas corruptas o truncadas tras registrar una advertencia de diagnóstico, sin descartar los registros válidos.
4. **Reconstrucción Idempotente:** Si `memoria.md` se corrompe o borra, `reconstruir_memoria(proyecto)` reconstruye el archivo completo preservando pendientes abiertos históricos, decisiones vigentes y la ventana de sesiones recientes.

---

## 5. Métricas Honestas de FinOps

El cálculo compara contextos equivalentes:
- `tokens_referencia`: tokens del prompt de contexto completo generado sin optimización (manifiesto + ADRs + memoria íntegra sin recortar).
- `tokens_enfocado`: tokens del prompt generado en modo enfocado (manifiesto + ADRs + estado activo + ventana deslizante).
- Método: Estimación de caracteres (~3.8 caracteres por token), reportado con transparencia.
- Fórmula:
  $$\text{Ahorro (\%)} = 100 \times \left(1 - \frac{\text{tokens\_enfocado}}{\text{tokens\_referencia}}\right)$$
- Almacenamiento en disco (`disco_bytes`, `disco_tokens`) se reporta por separado sin mezclarlo con el consumo de inferencia.
