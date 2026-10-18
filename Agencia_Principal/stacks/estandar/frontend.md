# Perfil estándar: Frontend

## Tecnología
React con JavaScript/JSX, Tailwind CSS, Lucide React, Sonner, Axios y React Router. Zustand solo si se necesita estado compartido. JSDoc para contratos cuando aporta claridad. Conservar las versiones instaladas; en un proyecto nuevo seleccionar versiones compatibles y verificadas. No introducir dependencias por seguir un ejemplo de una skill.

## Arquitectura y archivos
Aplicar [arquitectura frontend modular por dominio](arquitectura-frontend.md). Allí se definen módulos, archivos, componentes, hooks, servicios, estado y contratos públicos. Crear solo lo necesario. Conservar estructura real fuera del alcance autorizado; este perfil no ejecuta una migración.

## Simplicidad
Todo trabajo frontend aplica Ponytail en nivel `full` según la [política de simplicidad](../../reglas/simplicidad-ponytail.md): reutilizar antes de crear, controles HTML5 nativos, CSS/Tailwind y capacidades de React antes de nuevas dependencias, y ninguna abstracción, store o archivo sin necesidad actual.

## Integración y calidad
Aplicar el [contrato entre capas](contrato-integracion.md). Consumir DTOs backend, contemplar estados y comprobar accesibilidad y recorridos afectados. Build, lint y pruebas se obtienen del proyecto; distinguir revisión manual de validación automática.
