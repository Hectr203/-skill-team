---
name: atomic-design
description: Metodología de diseño atómico compositivo y modular para interfaces React. Guía para estructurar átomos, moléculas, organismos, plantillas y páginas sin sobreingeniería ni fragmentación excesiva.
---

# Atomic Design Compositivo en React

Esta skill proporciona las directivas para implementar Atomic Design en conjunto con la arquitectura de **Monorepo dividido** y **Feature-Driven Development** de la Agencia de Proyectos.

---

## 1. Niveles de Composición y Criterios de Creación

1. **Átomo**: Unidad visual mínima que no se puede descomponer sin perder su significado (`Button`, `Badge`, `InputText`, `Spinner`).
   - *Criterio de creación*: Debe usarse en al menos 2 moléculas o lugares distintos, o definir una variante visual consistente del sistema de diseño.
   - *Filtro Ponytail*: Si un elemento HTML estándar (`<span>`, `<label>`) con clases utilitarias es suficiente, **no crear un componente átomo**.
2. **Molécula**: Combinación cohesiva de 2 o más átomos para realizar una interacción simple (`FormField`, `SearchBar`, `InputGroup`).
   - Maneja validaciones locales inmediatas y emite eventos hacia el padre (`onChange`, `onSearch`).
3. **Organismo Neutro**: Estructuras visuales complejas que integran átomos y moléculas sin depender de una entidad de negocio (`ModalBase`, `DataTableBase`, `SidebarLayout`).
   - Ubicados en `src/shared/components/organisms/`.
4. **Componente de Dominio (Organismo Especializado)**:
   - Ubicados en `src/modules/<modulo>/<submodulo>/components/`.
   - Ensamblan los organismos neutros y átomos de `shared/`, inyectándoles datos, tipos y handlers específicos de la entidad.
5. **Página / Vista**:
   - `src/modules/<modulo>/<submodulo>/index.tsx`.
   - Conecta los custom hooks del submódulo con los componentes visuales de manera puramente declarativa.

---

## 2. Reglas de Dependencias entre Niveles

* Un átomo **nunca** importa una molécula u organismo.
* Una molécula **nunca** importa un organismo ni componentes de `modules/`.
* Un organismo neutro (`shared/`) **nunca** importa componentes de `modules/`.
* Los componentes de dominio en `modules/` pueden importar libremente cualquier nivel de `shared/components/`.
* Prohibido importar componentes privados entre distintos submódulos (ej. `modules/ventas` importando de `modules/almacenes/components/`).

---

## 3. Integración con Tokens y Google Stitch MCP

1. **Tokens de Diseño**:
   - Espaciado: escala de 4px (4, 8, 12, 16, 24, 32, 48, 64px).
   - Paletas: HSL o Hex semánticos (`primary`, `secondary`, `surface`, `danger`, `warning`, `success`).
   - Tipografía: Escala armónica (12, 14, 16, 20, 24, 32, 40px) con pesos estandarizados (400, 500, 600, 700).
2. **Design-to-Code desde Stitch**:
   - Inspeccionar la pantalla prototipada con Stitch MCP.
   - Mapear las regiones estructurales a los componentes de `shared/components/`.
   - Componer la vista en el submódulo correspondiente en `modules/`.
