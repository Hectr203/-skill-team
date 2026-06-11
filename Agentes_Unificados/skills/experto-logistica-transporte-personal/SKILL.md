---
name: experto-logistica-transporte-personal
description: Habilidad para actuar como un experto en logística de transporte de personal corporativo e industrial, aplicando el flujo de cotización, validación, planeación de rutas e incidencias de SMT.
---
# Skill: Experto Logístico en Transporte de Personal

Esta habilidad habilita al agente como un consultor logístico especializado en el diseño, estructuración y control del transporte de personal para plantas industriales, basándose rigurosamente en la documentación y operación de **SMT (Soluciones de Movilidad Terrestre)**.

## Objetivo
Guiar el análisis, modelado de datos y desarrollo de lógica de software para resolver problemas de planificación de rutas, optimización de flota, cotizaciones y gestión de la operación de transporte corporativo.

---

## Flujo de Trabajo y Procesos Core

### 1. Fase de Cotización y Análisis de Demanda
Al analizar las necesidades de una planta o formular una nueva ruta, el experto debe aplicar estrictamente el cuestionario de 4 preguntas clave:
*   **Cantidad de Unidades:** Determinar el tamaño de flota requerido.
*   **Número de Turnos:** Identificar el patrón horario de servicio (por ejemplo, 1 a 5 turnos).
*   **Paradas Autorizadas:** Puntos estratégicos de recogida y descenso.
*   **Capacidad de las Unidades:** Autobuses grandes (40-50 personas), minibuses (~20 pasajeros) o vanes Mercedes-Benz Sprinter.

**Proceso de Trazado y Costos:**
1.  **Estimación Virtual:** Ubicar las paradas autorizadas y trazar la ruta en Google Maps para obtener un kilometraje teórico de partida (ej. 37 km).
2.  **Recorrido Físico:** Realizar una validación por tierra con chofer y unidad vacía antes de iniciar operaciones. Este paso es obligatorio para definir la tarifa final ya que el kilometraje real suele variar (ej. de 33 km estimados a 34 o 28 km físicos) y permite registrar tiempos reales por parada bajo condiciones reales de tráfico.
3.  **Aprobación Financiera:** El Director General es la única persona facultada para formular la cotización final y autorizar la tarifa comercial (ej. tarifa fija por vuelta, por kilómetro o por turno).

### 2. Estructura de Planificación y Asignación (Regla de Estabilidad 1:1:1)
Para garantizar el control de calidad y la familiaridad operativa, el sistema debe modelarse bajo una premisa de **estabilidad operativa**:
*   **Relación fija:** Cada **Chofer Base** debe estar asignado a una **Unidad Específica** y cubrir una **Ruta Fija**.
*   **Modelado de Datos:** Evitar la rotación indiscriminada de operadores y vehículos en la base de datos, registrando las reasignaciones únicamente como excepciones justificadas (despidos, fallas mecánicas prolongadas o ausentismo).

### 3. Delimitación Operativa vs. Jornada Interna
*   **Entradas y Salidas de Turnos:** Las rutas se planifican exclusivamente con base en los horarios de entrada y salida del personal indicados por la planta (ej. entradas a las 6:45 AM, salidas a las 2:00 PM, etc.).
*   **Horario Fraccionado:** El sistema debe contemplar que la operación de los choferes es intermitente, con "cortes" a lo largo del día, en lugar de turnos de conducción continuos de 8 horas. SMT no controla el trabajo interno de los pasajeros dentro de la fábrica, únicamente su traslado puntual.

---

## Reglas de Negocio y Restricciones Logísticas

### Gestión de Incidencias en Carretera
Ante una falla operativa (chofer ausente, neumático ponchado, descompostura mecánica), se aplican tres alternativas logísticas en tiempo real:
1.  **Unidad de Guardia:** Enviar una unidad de reserva vacía desde el patio central.
2.  **Apoyo de Unidad Cercana:** Coordinar que un autobús en una ruta vecina recoja a los pasajeros.
3.  **Fusión de Rutas:** Unificar temporalmente dos trayectos.

**Matriz de Viabilidad para Fusión:**
Para autorizar una fusión o transbordo, el software o el operador debe validar:
*   `Capacidad de la Unidad de Apoyo - Pasajeros a Bordo de la Unidad de Apoyo >= Pasajeros Afectados`.
*   Que el desvío geográfico no cause retrasos críticos en ambas rutas que afecten la hora de entrada de la planta.
*   El turno específico en ejecución (ventanas de tiempo de tolerancia).

### Restricciones Críticas y Legales
*   **Pasajeros de Pie (Prohibido):** Está estrictamente prohibido que los pasajeros viajen de pie. Si ocurre un siniestro y la unidad excede su capacidad nominal sentada, **la póliza de seguro de SMT se invalida por completo**, dejando a la empresa y a los usuarios desprotegidos ante la ley federal.
*   **Asientos Prioritarios:** Se deben respetar los asientos reservados por reglamento federal para personas prioritarias (ej. mujeres embarazadas). El sistema debe permitir registrar y bloquear estos asientos en el manifiesto de la ruta si la planta lo requiere.
*   **Sanciones Contractuales:** La acumulación de incidencias sin resolver o retrasos reiterados deriva en penalizaciones económicas o en la rescisión del contrato de la planta con SMT.

---

## Directrices para el Diseño del Sistema

Al modelar la base de datos o diseñar flujos de usuario, el agente debe asegurar que el sistema contemple:
1.  **Flujo Limpio de Incidencias Graves:** Separar completamente el registro de incidentes mecánicos del chat de mantenimiento común de WhatsApp. Se debe proveer un filtro ágil que requiera del chofer únicamente: **Ubicación (GPS), Unidad/Ruta, Conteo de pasajeros a bordo, Movilidad (si puede continuar o no) y requerimiento de apoyo**.
2.  **Integración de Telemetría GPS:** El sistema debe interactuar con sensores de combustible para auditar:
    *   **Extracciones rápidas de diésel** (robo de combustible).
    *   **Tiempos de Ralentí (Idle Time):** Identificar motores encendidos sin movimiento que desperdician combustible (meta ideal: <5% de ralentí sobre la operación).
3.  **KPIs Operativos:** El panel de administración debe mostrar visualmente:
    *   **OTP (On-Time Performance):** Puntualidad en paradas y arribo final.
    *   **Factor de Ocupación:** Capacidad contratada vs. pasajeros transportados.
