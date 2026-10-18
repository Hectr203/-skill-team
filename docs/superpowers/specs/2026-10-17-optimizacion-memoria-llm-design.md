# Especificación de Diseño: Optimización Jerárquica y Ventana Deslizante de Memoria para LLMs

- **Fecha:** 2026-10-17
- **Área:** Motor de Contexto y Persistencia de Memoria de Proyecto
- **Ubicación:** `Agencia_Principal/scripts/memoria_proyecto.py`, `Agencia_Principal/scripts/arranque.py`, `Agencia_Principal/scripts/cierre.py`

---

## 1. Contexto y Objetivos

### 1.1 Problema
En `Agencia_Principal`, cada proyecto gestiona su memoria viva en `contexts/projects/<id>/memoria.md` y `.memoria/timeline.jsonl`. Anteriormente, el archivo `memoria.md` acumulaba texto de manera plana e indefinida tras cada ejecución de `cierre.py`. 

Al invocar `arranque.py --prime`, se inyectaba el contenido íntegro de `memoria.md` dentro del prompt de arranque ("Context Primer"). A medida que un proyecto evoluciona y acumula decenas de tareas, esto produce:
1. **Saturación de tokens:** Archivos de memoria de más de 30 KB (~9,000 a 15,000 tokens) inyectados en cada turno.
2. **Degradación de atención ("Lost in the Middle"):** Los modelos de lenguaje pierden foco sobre los requerimientos actuales y las decisiones vigentes al procesar extensas listas de tareas pasadas ya cerradas.
3. **Altos costos de inferencia (FinOps):** Consumo excesivo e innecesario de tokens de entrada.

### 1.2 Objetivo
Implementar un sistema de **memoria jerárquica con ventana deslizante y compactación progresiva** que:
1. Reduzca el consumo de tokens en el prompt de arranque entre un 70% y un 85%.
2. Garantice que el LLM reciba siempre el foco en el **Estado Activo**, las **decisiones arquitectónicas vigentes** y las **últimas 3 a 5 sesiones**.
3. Conserve intacto el 100% del historial detallado en `.memoria/timeline.jsonl` (máquina) y compacte los hitos pasados en Markdown.
4. Mantenga compatibilidad total con proyectos existentes, scripts CLI y herramientas MCP locales (`agencia_arranque`, `agencia_cierre`, `agencia_estado`).

---

## 2. Arquitectura de Datos y Formato de Memoria

### 2.1 Estructura Jerárquica de `memoria.md`
El archivo `memoria.md` se estructurará formalmente en cuatro secciones:

```markdown
# Memoria del Proyecto: <id>

- **ID de Proyecto:** `<id>`
- **Fecha de creación:** <ISO-8601>
- **Estado general:** <Activo/En progreso/Inicializado>

---

## 1. Estado Activo y Criterios Vigentes
- **Objetivo actual:** <Resumen del alcance activo>
- **Hito/Sprint:** <Fase actual de trabajo>
- **Pendientes consolidados:**
  - [ ] <Pendiente prioritario 1>
  - [ ] <Pendiente prioritario 2>
- **Decisiones clave vigentes:** <Síntesis de reglas técnicas acordadas>

---

## 2. Decisiones Técnicas y ADRs
- `<ADR-XXX>`: <Título de decisión arquitectónica>

---

## 3. Historial Reciente (Ventana Deslizante: Últimas N Sesiones)

### [<Fecha UTC>] Sesión / Tarea
- **Agente:** <Rol>
- **Tareas completadas:** <Detalle de tareas>
- **Archivos afectados:** `<ruta1>`, `<ruta2>`
- **Decisiones técnicas:** <Decisión>
- **Pendientes:** <Pendientes específicos de la tarea>
- **Riesgos:** <Riesgos detectados>

---

## 4. Hitos Anteriores (Bitácora Compactada)
- [<Fecha>] (<Agente>) <Hito sintético consolidado en 1 línea>
```

### 2.2 Almacén Inmutable (`.memoria/timeline.jsonl`)
- Todas las sesiones sin excepción se siguen guardando íntegras con formato JSON estructurado en `.memoria/timeline.jsonl` (y `cloudmem.jsonl`).
- Este archivo opera como la fuente de verdad inmutable y exhaustiva de auditoría.

---

## 3. Lógica y Flujo Operativo de Componentes

### 3.1 Motor de Memoria (`memoria_proyecto.py`)
1. **Detección de Secciones y Parsing:**
   - La función `analizar_memoria(contenido: str)` identifica las secciones principales mediante expresiones regulares robustas.
   - Si se encuentra un `memoria.md` antiguo con formato plano sin secciones formalizadas, el motor lo preserva de forma transparente y organiza el nuevo contenido a partir del primer cierre.
2. **Rotación y Compactación Automática (`rotar_memoria`):**
   - Umbral de ventana deslizante: 5 sesiones detalladas en la Sección 3.
   - Cuando un nuevo cierre agrega la 6ª sesión, la sesión más antigua de la ventana se compacta automáticamente a un hito de 1 línea y se transfiere a la Sección 4 (*Hitos Anteriores*).
   - Formato del hito compacto: `- [YYYY-MM-DD HH:MM] (<Agente>) <Resumen de tareas> (<N> archivos)`
3. **Escritura Atómica y Concurrencia:**
   - Se mantiene el uso de bloqueo exclusivo mediante `fcntl.flock` en `.memoria/.lock` y reemplazo atómico seguro con `os.replace`.

### 3.2 Context Engine y Generación de Prompt (`arranque.py`)
1. **Modo Estándar / Enfocado (`--prime`):**
   - `generar_primer_prompt()` inyecta:
     - Cabecera y métricas FinOps (tokens estimados y ahorro porcentual).
     - Manifiesto del proyecto (contrato y alcance).
     - Decisiones de Arquitectura (ADRs activos).
     - **Estado Activo y Ventana Deslizante:** Solo las Secciones 1, 2 y 3 de `memoria.md`.
     - Omite la bitácora histórica extensa de la Sección 4 para evitar ruido y consumo innecesario de tokens.
2. **Modo Historial Completo (`--completo`):**
   - Se introduce el flag `--completo` (ejemplo: `python3 scripts/agencia.py arranque <id> --prime --completo`).
   - Permite que un auditor o agente de revisión general recupere deliberadamente la totalidad de la bitácora compacta y el historial completo si lo necesita.
3. **Métricas de FinOps de Contexto:**
   - El cálculo de tokens compara el tamaño del prompt enfocado con el tamaño total acumulado en disco, informando en consola:
     `~1,150 tokens estimados (Ahorro del 76% vs 4,800 tokens totales en disco)`

### 3.3 Registro de Cierre (`cierre.py`)
1. Incorpora la actualización del bloque de estado activo cuando se indican nuevos pendientes o decisiones.
2. Ejecuta la rotación de sesiones manteniendo la integridad del archivo.

---

## 4. Compatibilidad, Seguridad y Manejo de Errores

### 4.1 Compatibilidad Retroactiva
- **Sin Breaking Changes:** Las interfaces de línea de comandos (`scripts/agencia.py`) y las herramientas del servidor MCP (`agencia_arranque`, `agencia_cierre`, `agencia_estado`) conservan estrictamente sus argumentos y contratos de salida.
- **Proyectos Existentes:** La lectura de proyectos existentes nunca sobrescribe ni corrompe memorias ya creadas.
- **Capa Cifrada:** El soporte opcional de cifrado Fernet (`mem_palace.enc`) se mantiene idéntico.

### 4.2 Robustez y Fallbacks
- Si `memoria.md` estuviera ausente o dañado, `arranque.py` reconstruye automáticamente la ventana deslizante a partir de las últimas entradas de `.memoria/timeline.jsonl`.
- Las escrituras fallidas se cancelan de manera segura sin dejar archivos temporales corruptos.

---

## 5. Estrategia de Pruebas y Criterios de Aceptación

### 5.1 Nuevas Pruebas Unitarias (`tests/test_memoria_optimizada.py`)
1. **Test de Compactación Automática:**
   - Registrar 7 cierres consecutivos en un proyecto temporal.
   - Verificar que `memoria.md` conserva exactamente las 5 sesiones más recientes en detalle y las 2 más antiguas compactadas en hitos de 1 línea.
2. **Test de Generación de Primer (`--prime`):**
   - Verificar que el texto generado para el LLM contiene el estado activo y las sesiones recientes, omitiendo los hitos históricos antiguos salvo que se use `--completo`.
3. **Test de Flag `--completo`:**
   - Verificar que con `--completo` se incluye la bitácora histórica completa.
4. **Test de Métricas FinOps:**
   - Validar que el reporte de tokens calcula correctamente el presupuesto y el porcentaje de ahorro.

### 5.2 Verificación Integral de la Agencia
- `python3 scripts/validar_agencia.py`: Código de salida 0 (`VALIDACION OK`).
- `python3 -m unittest discover tests/`: 100% de las pruebas (existentes y nuevas) aprobadas.
- `python3 scripts/agencia.py verificar`: Generación de evidencia local aprobada.
- `python3 scripts/agencia.py comprobar`: Confirmación de evidencia vigente.
