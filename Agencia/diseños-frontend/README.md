# Diseños Frontend — Referencias Visuales

Esta carpeta es la **fuente de verdad visual del proyecto**. Aquí se almacenan todas las referencias de diseño que el desarrollador frontend debe consultar antes de codificar cualquier interfaz.

## Propósito
Cuando el agente `agente-desarrollo` inicia trabajo de frontend, lee esta carpeta primero para aplicar el estilo correcto en lugar de inventar uno. Si una subcarpeta está vacía, el agente usa las convenciones del skill `ui-ux-pro-max`.

## Estructura

| Carpeta | Qué guardar aquí |
|---|---|
| [`efectos-y-animaciones/`](efectos-y-animaciones/) | Efectos hover, transiciones, animaciones con Tailwind que quieres |
| [`paletas-de-colores/`](paletas-de-colores/) | Colores primarios, secundarios, fondos y texto del proyecto |
| [`componentes-ui/`](componentes-ui/) | Capturas o descripciones de botones, cards, tablas, formularios de referencia |
| [`capturas-inspiracion/`](capturas-inspiracion/) | Screenshots de sitios, apps o diseños que el cliente quiere replicar |
| [`tailwind-config/`](tailwind-config/) | Clases custom, extensiones de `tailwind.config.js`, tipografías |

## Cómo agregar referencias

1. **Capturas de pantalla** → colócalas en `capturas-inspiracion/` con nombre descriptivo (ej. `login-dark-mode.png`).
2. **Efectos Tailwind** → descríbelos en `efectos-y-animaciones/efectos.md`.
3. **Colores** → agrégalos en `paletas-de-colores/paleta.md` en formato HEX o con nombre de Tailwind.
4. **Componentes de referencia** → agrega captura + descripción en `componentes-ui/`.

> El agente leerá estos archivos automáticamente cuando uses el skill `agente-desarrollo` con opción Frontend primero.
