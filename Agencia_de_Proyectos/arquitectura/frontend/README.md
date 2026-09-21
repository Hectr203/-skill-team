# Arquitectura del Frontend: Atomic Design Compositivo y Dominio Limpio

Esta guía establece el estándar arquitectónico para el desarrollo de aplicaciones frontend dentro de la Agencia de Proyectos. Combina **Feature-Driven Development / Dominio Limpio**, **Atomic Design Compositivo** y las mejores prácticas de la industria en **React**, **TypeScript** y **Vite / Next.js**.

---

## 1. Carácter de Arquetipo Ilustrativo y Adaptabilidad Universal

> [!IMPORTANT]
> **Arquetipo de referencia, no un dominio impuesto**:
> Las carpetas y nombres de dominios mostrados como ejemplo (tales como `almacenes`, `auditoria`, `inventario`) constituyen **únicamente un caso de estudio ilustrativo**. **NO representan un proyecto final real ni limitan a la agencia a crear sistemas de gestión o inventarios.**
>
> Ante cada nuevo proyecto, la agencia analizará los requisitos específicos del usuario (e-commerce, SaaS, fintech, streaming, salud, educación, etc.) deduciendo y modelando sus **propios dominios de negocio en español** (ej. en educación: `cursos`, `estudiantes`, `certificados`; en e-commerce: `catalogo`, `carrito`, `pagos`, `envios`).

---

## 2. Convención de Idioma y Nomenclatura

Para garantizar legibilidad inmediata y cero Spanglish desordenado:

* **Carpetas Estructurales y Técnicas en INGLÉS**:
  `src`, `config`, `modules`, `components`, `services`, `types`, `routes`, `middlewares`, `utils`, `shared`, `store`, `hooks`.
* **Dominios de Negocio y Submódulos SIEMPRE en ESPAÑOL**:
  Toda carpeta funcional que represente un concepto de negocio se nombra en español adaptado al giro del software:
  - En ERP / Gestión (ejemplo): `administracion`, `almacen`, `auth`, `compras`, `pedido`.
  - En E-Commerce: `catalogo`, `carrito`, `pagos`, `envios`, `clientes`.
  - En Salud / Clínicas: `pacientes`, `citas`, `historiales`, `medicos`.
  - En EdTech: `cursos`, `estudiantes`, `evaluaciones`.
* **Frontera Limpia**: La técnica habla el estándar global de la industria (`services`, `types`, `hooks`), mientras que el dominio refleja con exactitud el vocabulario del negocio en español.

---

## 3. Arquetipo Canónico Universal

```text
frontend/src/
├── assets/                                  # Imágenes, íconos SVG globales, tipografías
├── config/                                  # Configuración de la app y validación (.env con Zod)
├── modules/                                 # MÓDULOS DE DOMINIO DE NEGOCIO (Descubiertos por proyecto)
│   └── <modulo-del-negocio>/                # Carpeta en español del dominio (ej. ventas, pacientes, catalogo)
│       └── <submodulo>/                     # Subdominio cohesivo (ej. facturacion, citas, productos)
│           ├── components/                  # Organismos y vistas ensambladas específicas del submódulo
│           │   ├── Modal<Accion><Submodulo>.tsx
│           │   └── Tabla<Submodulo>.tsx
│           ├── hooks/                       # Lógica reactiva, debounce, paginación local (use<Submodulo>.ts)
│           ├── services/                    # Llamadas a API tipadas específicas de este submódulo
│           │   └── <submodulo>Service.ts
│           ├── types/                       # Interfaces TypeScript y contratos de datos del submódulo
│           │   └── <submodulo>Types.ts
│           └── index.tsx                    # Vista principal / Página del submódulo (Page / View)
├── shared/                                  # RECURSOS GLOBALES Y ATOMIC DESIGN SYSTEM
│   ├── components/                          # Componentes de UI puros, reutilizables y sin lógica de negocio
│   │   ├── atoms/                           # Bloques básicos: Button, Input, Badge, Spinner, Checkbox
│   │   ├── molecules/                       # Combinaciones simples: FormField, SearchBar, SelectBase, Dropdown
│   │   └── organisms/                       # Ensamblajes complejos: ModalBase, DataTableBase, Navbar, Sidebar
│   ├── hooks/                               # Hooks reutilizables globales: useDebounce, useMediaQuery, useToast
│   ├── services/                            # Cliente HTTP base (Axios/Fetch) con interceptores y token refresh
│   ├── store/                               # Estado global de sesión y preferencias (Zustand / Redux Toolkit)
│   ├── theme/                               # Tokens de diseño sincronizados con Google Stitch (colores, tipografía)
│   └── utils/                               # Formateadores (moneda, fechas), validadores y helpers puros
├── routes/                                  # Enrutador centralizado de la aplicación (React Router)
├── App.tsx                                  # Componente raíz con proveedores globales (Theme, QueryClient, Auth)
└── main.tsx                                 # Punto de entrada de Vite / React
```

---

## 4. Atomic Design Compositivo: Niveles y Responsabilidades

Inspirado en los principios de Brad Frost y adaptado a aplicaciones ricas:

1. **Átomos (`shared/components/atoms/`)**:
   - Bloques indivisibles de interfaz gráfica: `Button`, `Input`, `Badge`, `Spinner`, `Checkbox`, `Typography`.
   - Regla: Cero dependencias de lógica de negocio o servicios. Estilos puros parametrizados por props.
   - **Filtro Ponytail**: No envolver etiquetas nativas HTML (`<button>`, `<input>`) en wrappers vacíos si no aportan variantes de diseño o accesibilidad demostrada.
2. **Moléculas (`shared/components/molecules/`)**:
   - Grupos simples de átomos funcionando como una unidad: `FormField` (Label + Input + ErrorText), `SearchBar` (Input + SearchIcon + ClearButton), `PaginationControls`.
3. **Organismos Neutros (`shared/components/organisms/`)**:
   - Secciones de interfaz reutilizables sin acoplamiento a una entidad concreta: `ModalBase`, `DataTableBase`, `HeaderLayout`, `SidebarLayout`.
4. **Componentes y Organismos de Dominio (`modules/<modulo>/<submodulo>/components/`)**:
   - Ensamblajes especializados creados para un submódulo específico: `TablaAuditoria.tsx`, `ModalCrearAlmacen.tsx`.
   - Componen los átomos, moléculas y organismos neutros de `shared/`, inyectándoles los tipos y eventos del dominio.
5. **Páginas / Vistas (`modules/<modulo>/<submodulo>/index.tsx`)**:
   - Punto de entrada de la ruta. Conecta los custom hooks del submódulo con los componentes visuales de manera puramente declarativa.

---

## 5. Reglas de Oro y Patrones de Excelencia

1. **Encapsulamiento de Dominio (Domain Boundaries)**:
   - Los componentes en `modules/<modulo>/<submodulo>/components/` son **privados**. Ningún otro módulo debe importarlos directamente.
   - Si un componente requiere ser reutilizado en múltiples dominios, se promueve a `shared/components/`.
2. **Servicios y Tipos Desacoplados**:
   - Cada submódulo tiene sus propios `services/` y `types/`. Se prohíbe el antipatrón de concentrar todas las llamadas de API de la empresa en un único archivo monstruoso.
   - Todos los servicios de submódulo consumen la instancia HTTP centralizada de `shared/services/`.
3. **Separación Estricta de Lógica y UI con Custom Hooks**:
   - La gestión de estado reactivo complejo (filtros combinados, paginación, debounce de búsqueda, apertura/cierre de modales) se encapsula en un hook local (ej. `hooks/useAlmacenes.ts`).
   - El archivo `index.tsx` se mantiene declarativo, limpio y fácilmente testeable.
4. **Diseño Responsivo y Accesibilidad (a11y)**:
   - Toda interfaz debe verificarse en tres vistas clave: Desktop (1280px+), Tablet (768px-1024px) y Móvil (375px-430px).
   - Uso de atributos semánticos (`aria-label`, `aria-expanded`, navegación completa por teclado).
   - Respeto incondicional a la directiva `prefers-reduced-motion` para usuarios sensibles a animaciones.

---

## 6. Integración con Google Stitch MCP

1. **Ideación e Inspección**: Generación y consulta de prototipos UI mediante el servidor Stitch MCP.
2. **Extracción de Design Tokens**: Extracción automatizada de paletas de color, tipografía y espaciado para alimentar `src/shared/theme/` y variables CSS/Tailwind.
3. **Mapeo Atómico**: Descomposición de las pantallas de Stitch en átomos y moléculas de `shared/components/`, y organismos en las vistas de `modules/`.
4. **Traducción a Código Limpio**: Generación de componentes tipados en React/TypeScript sin código espagueti ni librerías no solicitadas.
