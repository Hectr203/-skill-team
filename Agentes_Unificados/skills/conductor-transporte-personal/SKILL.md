---
name: conductor-transporte-personal
description: Habilidad para simular y comprender la psicología, comportamiento, limitaciones digitales y responsabilidades del conductor (chofer) de transporte de personal en SMT.
---
# Skill: Conductor de Transporte de Personal

Esta habilidad permite al agente comprender y adoptar la perspectiva del operador de transporte (chofer) de SMT, considerando sus retos diarios, sus limitaciones técnicas frente a herramientas digitales y sus prioridades de seguridad en carretera.

## Objetivo
Asegurar que los diseños de interfaz, flujos de datos y sistemas de comunicación dirigidos a los choferes sean sencillos, prácticos y adaptados a su realidad laboral, evitando la fricción tecnológica y garantizando reportes de incidencias rápidos y precisos.

---

## Perfil del Operador y Factores Humanos

### 1. Brecha de Alfabetización Digital
*   **Limitaciones en Lectoescritura:** Una proporción significativa de los operadores de SMT cuenta con baja escolaridad, teniendo serias dificultades para escribir textos detallados, leer manuales extensos o interactuar con menús digitales complejos.
*   **Preferencia por el Canal de Voz:** Ante cualquier imprevisto en carretera o reporte operativo, los choferes prefieren realizar una llamada telefónica o enviar un mensaje de voz en WhatsApp en lugar de redactar reportes escritos.
*   **Facilidad de Uso:** Las interfaces de software diseñadas para el operador deben ser extremadamente visuales, con botones de gran tamaño, iconos descriptivos y mínimo requerimiento de entrada de texto manual.

### 2. Prioridad de Conducción y Presión Operativa
*   **Responsabilidad de Seguridad:** La tarea primordial y excluyente del operador es conducir con precaución y salvaguardar la integridad física de los 20 a 55 pasajeros a bordo de la unidad.
*   **Atención Dividida:** Está prohibido que el operador manipule el teléfono celular mientras conduce. Exigir reportes constantes o detallados durante el trayecto incrementa el riesgo de accidentes y genera retrasos operativos de 5 a 15 minutos en la ruta.
*   **Protocolo de Parada Segura:** El chofer solo responderá o enviará información digital cuando la unidad se encuentre completamente estacionada en un punto de parada seguro o en la planta.

---

## Responsabilidades y Preocupaciones del Chofer

### 1. Responsabilidad sobre la Unidad y Ruta Fija (Regla 1:1:1)
*   **Cuidado del Activo:** Al tener asignado un autobús o van permanente (vincular de forma fija chofer-unidad), el operador se responsabiliza de entregarla limpia, reportar fallas mecánicas a tiempo y cuidar de los neumáticos y niveles de fluidos.
*   **Conocimiento del Trayecto:** El operador se familiariza con el mapa de paradas de su ruta específica, memorizando los nombres de las paradas, los tiempos estimados entre ellas y las condiciones viales de su recorrido habitual.

### 2. Normas de Seguridad en Cabina
*   **Capacidad Sentada Obligatoria:** El chofer tiene la responsabilidad de negar el acceso a pasajeros cuando la unidad ya no cuente con asientos disponibles. Permitir pasajeros de pie expone al chofer a infracciones de tránsito federales, reportes por parte de la planta, y la invalidación total del seguro de pasajeros ante un siniestro.
*   **Asientos Prioritarios:** El operador debe asegurarse de que se respeten los asientos asignados para personas prioritarias (ej. mujeres embarazadas de la planta), gestionando de manera asertiva el comportamiento de los pasajeros en cabina.

### 3. Presión en la Gestión de Combustible
*   **Alertas de Telemetría:** El chofer sabe que el consumo de diésel está siendo monitoreado por GPS. Debe evitar prácticas de conducción ineficientes como el **ralentí excesivo** (mantener el motor encendido mientras espera la salida del turno de la planta), ya que SMT sanciona estas conductas.

---

## Directrices para el Diseño del Canal del Conductor

Al implementar flujos donde intervenga el conductor (ej. reportar inicio de ruta, llegada a planta o incidencias), el agente debe aplicar las siguientes reglas:
1.  **Formulario Simplificado de Incidencias Graves:** Ante una avería mecánica en ruta, el chofer NO debe explicar detalles de ingeniería automotriz. El sistema debe solicitarle únicamente 3 toques en pantalla:
    *   *Ubicación:* GPS del teléfono (compartir ubicación actual con un botón).
    *   *Pasajeros a bordo:* Seleccionar un número rápido de usuarios (ej. deslizador o botones rápidos).
    *   *Estado de Movilidad:* Botones simples: "Inmovilizado" / "Avanzando lento".
    *   *Solicitud:* "Requiere unidad de guardia" / "Requiere auxilio mecánico".
2.  **Reportes Rápidos de Ruta:** Diseñar los reportes de inicio, planta y fin de ruta mediante botones de un solo toque apoyados por geolocalización automática:
    *   *Ejemplo de flujo:* El operador presiona un gran botón verde de "Iniciar Recorrido", y el sistema captura automáticamente la hora y coordenadas GPS sin requerir escritura.
3.  **Alertas de Voz:** Priorizar el uso de notificaciones auditivas claras en lugar de mensajes de texto en pantalla para alertar al operador sobre cambios en la ruta antes de que encienda el motor.
