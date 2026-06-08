---
name: desarrollador-frontend
description: Habilidad para construir interfaces de usuario responsivas, interactivas y conectar la aplicación cliente con el backend.
---
# Skill: Desarrollador Frontend

Esta habilidad orienta al agente para construir la capa de presentación de la aplicación. Se centra en la experiencia del usuario (UX), la interfaz de usuario (UI), el diseño responsivo y la integración fluida con las APIs.

## Cuándo usar esta habilidad
Utiliza esta habilidad cuando la tarea implique:
- Creación de nuevas pantallas, vistas o componentes visuales.
- Estilización de la aplicación (CSS, Tailwind, SASS, Styled Components).
- Gestión del estado del lado del cliente (Redux, Zustand, Context API).
- Consumo de APIs (fetch, Axios, React Query) y renderizado dinámico de datos.
- Mejora de la accesibilidad (a11y) o del rendimiento visual.

## Objetivo
Implementar interfaces de usuario atractivas, rápidas y accesibles, traduciendo los diseños y requerimientos a código que funcione perfectamente en distintos navegadores y dispositivos.

## Flujo de Trabajo

1.  **Análisis de UI/UX**:
    - Revisa las Historias de Usuario y cualquier mockup o guía de estilo proporcionada.
    - Identifica los componentes reutilizables necesarios.

2.  **Desarrollo de Componentes**:
    - Construye los componentes visuales asegurándote de que sean responsivos (Mobile First generalmente).
    - Aplica estilos de manera consistente y organizada.

3.  **Integración y Estado**:
    - Conecta los componentes con las APIs desarrolladas por el `desarrollador-backend`.
    - Maneja los diferentes estados de la UI (Cargando, Error, Éxito, Vacío).
    - Gestiona el estado global y local de forma eficiente.

4.  **Validación**:
    - Verifica el diseño en diferentes tamaños de pantalla.
    - Asegura que los formularios tengan validaciones del lado del cliente antes de enviarlos.

## Reglas y Restricciones
- Crea componentes pequeños, de una sola responsabilidad (Single Responsibility Principle).
- Mantén el código limpio, estructurado y evita la duplicidad de estilos.
- Proporciona retroalimentación visual al usuario en todo momento (ej. spinners durante la carga, mensajes de error legibles).
- Extrae la lógica compleja fuera de los componentes visuales (por ejemplo, usando custom hooks en React).
