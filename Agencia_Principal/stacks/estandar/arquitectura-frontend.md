# Arquitectura frontend: módulos de negocio

## Alcance
El perfil estándar organiza el frontend por módulos de negocio. Cada módulo reúne presentación, lógica, servicios, estado y contratos. Se conserva la estructura propuesta por el usuario; no se reparte un mismo módulo entre capas globales. En proyectos existentes mejorar únicamente el alcance autorizado, sin declarar una migración aplicada por actualizar estos documentos.

## Simplicidad obligatoria (Ponytail)
Todo trabajo frontend aplica la skill Ponytail en nivel `full` según la [política de simplicidad](../../reglas/simplicidad-ponytail.md). Ponytail actúa dentro de esta arquitectura modular: prohíbe crear carpetas o archivos vacíos (`store/`, `types/`, `hooks/`), wrappers artificiales, proveedores innecesarios o micro-componentes prematuros. Si una funcionalidad se resuelve con un componente y estado local `useState`, no se añade un store global ni se extraen hooks artificiales sin reutilización. Controles HTML5 nativos y estilos utilitarios se prefieren antes de nuevas librerías. Las pruebas son proporcionales al riesgo: comprobaciones ejecutables para lógica de cliente no trivial, sin suites redundantes.

## Árbol de archivos

```text
frontend/
└── src/
    ├── app/
    │   ├── App.jsx
    │   ├── rutas.jsx
    │   └── proveedores.jsx
    ├── components/
    │   ├── ui/
    │   ├── layout/
    │   ├── feedback/
    │   └── data-display/
    ├── modules/
    │   └── administracion/
    │       └── almacen/
    │           ├── components/
    │           ├── hooks/
    │           ├── services/
    │           ├── store/
    │           ├── types/
    │           └── index.jsx
    ├── hooks/
    ├── services/
    │   └── clienteApi.js
    ├── types/
    ├── utils/
    └── index.jsx
```

`administracion/almacen` es un ejemplo de área y módulo; usar nombres propios del dominio del proyecto. Crear solo carpetas y archivos necesarios, sin esqueletos vacíos. Configuración de herramientas y dependencias vive en la raíz frontend según el proyecto.

## Responsabilidades
- `src/index.jsx`: arranque del frontend y montaje de la aplicación.
- `app/App.jsx`: composición raíz. `rutas.jsx` define navegación y conecta entradas de módulos. `proveedores.jsx` configura proveedores globales.
- `components/ui`: controles genéricos. `layout`: estructura visual reutilizable. `feedback`: estados y diálogos. `data-display`: presentación genérica de datos. No conocen endpoints, stores ni reglas de un módulo.
- `modules/<area>/<modulo>/components`: componentes propios del negocio, sin reproducir por obligación las categorías globales.
- `hooks`: coordinación de casos de uso, formularios, carga y acciones del módulo.
- `services`: endpoints y mapeo de contratos de ese módulo; consumen el cliente común.
- `store`: estado del módulo cuando requiere consumidores compartidos; opcional. Estado local para interacciones locales y URL para filtros compartibles.
- `types`: contratos JSDoc en `.js` para el perfil JavaScript; opcional. No valida datos en ejecución.
- `index.jsx` del módulo: entrada visual pública que compone su pantalla. Si hacen falta otros contratos públicos, exponerlos explícitamente sin exportar indiscriminadamente todos los interiores.
- `hooks`, `services`, `types` y `utils` globales: recursos con reutilización real entre módulos. No alojan negocio específico; `services/clienteApi.js` centraliza configuración HTTP.

## Dependencias y encapsulación
`app` compone entradas públicas de módulos. Cada módulo usa sus propios recursos y los compartidos. Los recursos globales no importan módulos. Un módulo no accede a archivos internos de otro; si necesitan colaborar, acordar un contrato público explícito o componer la interacción desde la aplicación. Evitar ciclos y stores globales que mezclen contextos de clientes. No extraer lógica al nivel global solo por el tamaño del archivo.

## Flujo y contratos
El recorrido habitual es pantalla → hook del caso de uso → servicio del módulo → cliente HTTP común → API. Una interacción visual sencilla puede permanecer local. Los servicios devuelven datos o errores, sin renderizar ni emitir notificaciones. Los componentes no contienen consultas HTTP ni reglas backend. Acordar DTOs públicos, rutas, permisos, errores, paginación, fechas y precisión monetaria con backend; no consumir modelos ORM internos.

Definir una fuente de verdad e invalidación de datos tras mutaciones. Evitar dobles envíos y cancelar o descartar respuestas obsoletas. Limpiar datos al cambiar de cliente o sesión. La autorización efectiva y las reglas de negocio se validan en el servidor.

## Calidad y entrega
Comprobar carga, vacío, error, éxito y permisos; conservar datos ante errores recuperables. Revisar teclado, labels, foco, contraste, modales y movimiento reducido. No asumir capacidades por estereotipos. Ejecutar build, lint y pruebas pertinentes disponibles, describiendo controles manuales y pendientes sin inventar herramientas. Entregar módulos y recursos compartidos afectados, contratos, cambios y evidencia real.

Este contrato describe una arquitectura modular por dominio; no usa las capas globales de Feature-Sliced Design. La tecnología corresponde a [frontend.md](frontend.md), y los acuerdos entre capas a [contrato-integracion.md](contrato-integracion.md).
