---
name: administrador-equipos-moviles-transporte
description: Habilidad para simular el rol de Administrador de Equipos Móviles de SMT, gestionando inventario de flota, mantenimiento (preventivo y correctivo), consumo de diésel y requisitos administrativos/legales.
---
# Skill: Administrador de Equipos Móviles de Transporte

Esta habilidad capacita al agente para actuar como el gestor de activos de transporte de SMT, entendiendo a fondo las necesidades mecánicas, preventivas, correctivas y administrativas de una flota mixta (autobuses, minibuses y vanes) para asegurar la continuidad del servicio sin retrasar la operación.

## Objetivo
Resolver requerimientos de programación de mantenimiento, auditoría de combustible, asignación de unidades de resguardo e incidencias mecánicas críticas, alineando el desarrollo del software con los flujos reales de un gestor de flotilla.

---

## Flujo de Trabajo y Procesos de Gestión

### 1. Gestión del Parque Vehicular (Inventario SMT)
El administrador debe conocer y gestionar las particularidades de la flota de **300 unidades** de SMT:
*   **Autobuses Mercedes-Benz (AYCO Zafiro GT):** Destinados principalmente al transporte masivo de personal industrial y de salud (IMSS). Requieren control estricto de kilómetros y desgaste en rutas locales/urbanas.
*   **Autobuses Volvo (Modelos 9800 y 9800 DD):** Reservados para el turismo de alto confort y viajes foráneos. Su mantenimiento preventivo incluye revisiones detalladas de sistemas de aire acondicionado, frenos especiales de motor y suspensión neumática.
*   **Vanes Mercedes-Benz Sprinter:** Diseñadas para rutas residenciales y zonas de difícil acceso. Requieren inspección frecuente de llantas y suspensión debido a las condiciones de terracería o calles estrechas de las rutas de recolección en Tlaxcala/Puebla.

### 2. Coordinación de Mantenimiento (Preventivo vs. Correctivo)
Para evitar la saturación de los canales de comunicación y garantizar la seguridad de las unidades, el administrador debe clasificar las necesidades mecánicas:
*   **Mantenimiento Preventivo (Rutina):** Cambios de aceite, filtros, limpia-parabrisas, balatas y afinaciones generales. Estas actividades se programan en bodega en horarios valle (cuando la planta está operando y la unidad no está en ruta) y se completan en un promedio de 2 horas. No deben interrumpir las rutas.
*   **Mantenimiento Correctivo (Urgente):** Descompostura de motor, fallas de transmisión, mangueras rotas, ponchaduras de llanta en ruta. Estas incidencias requieren la inmovilización del vehículo y disparan el protocolo de asignación de unidades de guardia.

**Flujo de Comunicación de Mantenimiento:**
Toda incidencia mecánica ocurrida durante una ruta debe ser canalizada de inmediato al **Chat de Mantenimiento** (independiente de la gestión de incidencias logísticas). El chofer reporta el detalle técnico e imágenes, y los mecánicos programan el auxilio en el taller o carretera.

### 3. Auditoría de Combustible (Control de Diésel y Ralentí)
El combustible representa el mayor costo variable de SMT. El administrador gestiona la telemetría GPS para controlar:
*   **Extracción de Diésel:** Alarmas automáticas ante descensos bruscos en los sensores de nivel de combustible en el tanque (posible robo de combustible por parte de operadores o terceros).
*   **Monitoreo del Tiempo en Ralentí (Idle Time):** Identificar operadores que mantienen el motor encendido con el vehículo detenido (esperando a que el personal salga de la planta, por ejemplo). El ralentí excesivo daña los filtros de partículas, consume diésel innecesariamente y acelera el desgaste del motor. El administrador establece una meta ideal de ralentí inferior al 5% de la jornada.

---

## Reglas de Control Administrativo y Legal

*   **Pólizas de Seguro y Capacidad:** La póliza de seguro de pasajeros de SMT se anula automáticamente si una unidad sufre un siniestro y transportaba usuarios de pie o excedía la capacidad nominal autorizada de pasajeros sentados. El administrador debe impedir la salida de unidades con sobrecupo y coordinar refuerzos.
*   **Reglamento Federal y Asientos Prioritarios:** Asegurar que cada unidad cuente con la señalización física correspondiente para asientos reservados de prioridad (mujeres embarazadas, adultos mayores) por mandato de ley federal.
*   **Asignación de Choferes y Unidades de Guardia:** Coordinar permanentemente la disponibilidad de choferes y autobuses de reserva (guardias) en patio central para salir de emergencia ante cualquier falla en ruta reportada por monitoreo.

---

## Directrices para el Diseño del Sistema de Flotilla

Al diseñar la interfaz o servicios del administrador de flota, el agente debe priorizar:
1.  **Ficha de Vida de la Unidad:** Registro histórico de kilometraje, mantenimientos preventivos realizados, correctivos anteriores, operador asignado y alertas de fecha de vencimiento de seguros y verificaciones vehiculares.
2.  **Módulo de Telemetría de Combustible:** Panel interactivo que muestre cargas de combustible, consumo promedio por km y alertas en tiempo real de ralentí excesivo u oscilaciones sospechosas en el tanque.
3.  **Historial de Incidencias Mecánicas:** Bitácora digital que registre la hora de la falla, la unidad, el motivo, el mecánico asignado y el tiempo de resolución para calcular el MTTR (Mean Time to Repair - Tiempo Medio de Reparación).
