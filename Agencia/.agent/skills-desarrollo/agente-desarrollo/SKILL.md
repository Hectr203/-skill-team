---
name: agente-desarrollo
description: Orquesta el inicio de cualquier tarea de desarrollo. Pregunta al usuario si desea empezar por el Frontend (presentación visual/mockup) o por el Backend (APIs/base de datos) antes de delegar al especialista correspondiente.
---
# Skill: Agente de Desarrollo

Este skill actúa como punto de entrada para cualquier tarea de implementación técnica. Su responsabilidad principal es **preguntar siempre al usuario cómo desea iniciar** antes de delegar trabajo a los desarrolladores especializados.

## Cuándo usar esta habilidad
Utiliza esta habilidad cuando:
- Se va a iniciar el desarrollo de un requerimiento ya documentado.
- El usuario pide "comenzar a desarrollar", "implementar" o "codificar" una funcionalidad.
- Se necesita decidir el orden de implementación (Frontend primero vs Backend primero).

## REGLA OBLIGATORIA: Pregunta de Inicio

**Antes de escribir una sola línea de código, SIEMPRE debes hacer esta pregunta al usuario:**

---
> **¿Por dónde deseas comenzar el desarrollo?**
>
> **[1] Frontend primero** — Construir la interfaz visual, mockup o prototipo funcional primero.
> - Ideal cuando el cliente necesita ver cómo quedará la pantalla antes de validar.
> - Se crean componentes, vistas y estados de UI con datos simulados (mock data).
> - Permite presentar una demo visual sin que el backend esté listo.
>
> **[2] Backend primero** — Construir las APIs, base de datos y lógica de negocio primero.
> - Ideal cuando ya se tiene claridad del diseño y se prioriza la funcionalidad.
> - Se crean endpoints, modelos Prisma, servicios y controladores.
> - El frontend se conecta a APIs reales desde el inicio.

---

Espera la respuesta del usuario antes de continuar.

## Flujo de Trabajo

### Si el usuario elige [1] Frontend primero:
1. Activa el skill `desarrollador-frontend`.
2. Consulta la carpeta `Agencia/diseños-frontend/` para obtener las referencias visuales, efectos y clases Tailwind que el usuario quiere aplicar.
3. Construye los componentes con **mock data** (datos simulados) para poder hacer la demo sin backend.
4. Al terminar la presentación/validación, activa `desarrollador-backend` para conectar las APIs reales.

### Si el usuario elige [2] Backend primero:
1. Activa el skill `desarrollador-backend` con el skill de soporte `backend-dominio-limpio`.
2. Implementa las APIs, modelos Prisma y lógica de negocio.
3. Una vez listos los endpoints, activa `desarrollador-frontend` para construir la UI conectada a datos reales.

## Consulta de Referencias de Diseño

Cuando se trabaja en el frontend, **siempre revisa** la carpeta `Agencia/diseños-frontend/` antes de codificar:

```
Agencia/diseños-frontend/
├── efectos-y-animaciones/   → Efectos Tailwind a aplicar (hover, transition, etc.)
├── paletas-de-colores/      → Paletas de color aprobadas por el cliente
├── componentes-ui/          → Capturas o descripciones de componentes de referencia
├── capturas-inspiracion/    → Imágenes de diseño que el cliente quiere replicar
└── tailwind-config/         → Configuración personalizada de Tailwind y clases custom
```

Si la carpeta tiene referencias, úsalas como guía de estilo. Si está vacía, aplica las convenciones del skill `ui-ux-pro-max`.

## Reglas y Restricciones
- **Nunca** comiences a implementar sin haber preguntado frontend vs backend.
- Si el cliente solo pidió "hacer el diseño" o "mostrar cómo se va a ver", siempre va Frontend primero.
- Si el cliente mencionó explícitamente APIs, base de datos o lógica de negocio, sugiere Backend primero pero confirma con el usuario.
- Mantén comunicación continua con el usuario sobre el avance y los próximos pasos.
