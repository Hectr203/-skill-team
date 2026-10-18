# Plantilla para Registro de Nuevo Stack Tecnológico

Utilice esta plantilla al registrar un nuevo ecosistema o perfil tecnológico bajo `stacks/alternativos/<id_stack>/`.

---

## 1. Identificación del Stack
- **Nombre Formal:** [Ejemplo: Laravel + Livewire + Alpine.js]
- **Identificador Único (`id`):** [ejemplo: laravel-livewire-alpine]
- **Versiones Oficiales:** [Ejemplo: PHP 8.3+, Laravel 11/12, Livewire 3.5+, Alpine.js 3.14+]
- **Justificación de Uso:** [¿Por qué este proyecto requiere este stack y no el estándar?]

---

## 2. Dependencias y Paquetes Clave
```json
// O composer.json / pyproject.toml / etc.
```

---

## 3. Estructura de Directorios Recomendada
```txt
// Árbol de carpetas del proyecto para este stack
```

---

## 4. Contratos de Arquitectura y Persistencia
- **Capa de Negocio / Dominio:** [Convenciones de servicios, modelos, acciones]
- **Persistencia / ORM:** [Eloquent, SQLAlchemy, etc. - Reglas de migración]
- **Interfaz de Usuario:** [Blade, Templates, Componentes, Estilos]
- **Convenciones de Idioma:** [Español para nombres propios nuevos y comunicación, conservando convenciones y contratos existentes]

---

## 5. Estrategia de Pruebas y Validación
- **Runner de Pruebas:** [Pest, PHPUnit, Pytest, etc.]
- **Comandos de Verificación:**
  ```bash
  # Comando de linter / typecheck
  # Comando de pruebas unitarias
  ```


## 6. Resolución de capas e integración
- **Frontend:** [entrada o sección con arquitectura, archivos, imports y validación; no aplicable si no existe].
- **Backend:** [entrada o sección con dominio, casos de uso, interfaces/adaptadores y dependencias].
- **Datos:** [entrada o sección con esquema, migraciones, integridad y recuperación].
- **Contratos entre capas:** [DTOs públicos, errores, permisos, datos y responsables].
- **Estado existente / objetivo:** [distinguir estructura real de una migración propuesta].
- **Skills pertinentes y exclusiones:** [según tecnología y resultado, no heredadas del estándar automáticamente].
- **Desviaciones y ADRs:** [decisiones particulares sin duplicar contratos].

Los agentes referencian estas definiciones; no incorporan tecnologías fijas en sus fichas. Los comandos deben existir en el proyecto y una capa sin uso debe marcarse expresamente como no aplicable.
