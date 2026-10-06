# Stack Alternativo: Laravel 11/12 + Livewire 3 + Alpine.js + Tailwind CSS

Este documento define las especificaciones técnicas obligatorias cuando un proyecto se inicialice bajo el stack `laravel-livewire-alpine`.

---

## 1. Identificación y Justificación
- **Identificador (`id`):** `laravel-livewire-alpine`
- **Componentes Principales:** PHP 8.3+, Laravel 11/12, Livewire 3, Alpine.js 3, Tailwind CSS, ApexCharts.
- **Caso de Uso:** Aplicaciones web monolíticas de alto rendimiento interactivo con renderizado del lado del servidor sin sobrecarga de frameworks SPA desacoplados.

---

## 2. Dependencias Principales

### `composer.json` (PHP)
```json
{
  "require": {
    "php": "^8.3",
    "laravel/framework": "^11.0|^12.0",
    "livewire/livewire": "^3.5",
    "spatie/laravel-permission": "^6.0"
  },
  "require-dev": {
    "fakerphp/faker": "^1.23",
    "larastan/larastan": "^2.9",
    "mockery/mockery": "^1.6",
    "nunomaduro/collision": "^8.0",
    "pestphp/pest": "^2.34",
    "pestphp/pest-plugin-laravel": "^2.3"
  }
}
```

### `package.json` (JavaScript / UI)
```json
{
  "devDependencies": {
    "@tailwindcss/forms": "^0.5.7",
    "@tailwindcss/typography": "^0.5.10",
    "alpinejs": "^3.14.0",
    "apexcharts": "^3.50.0",
    "autoprefixer": "^10.4.19",
    "axios": "^1.7.0",
    "laravel-vite-plugin": "^1.0.0",
    "postcss": "^8.4.38",
    "tailwindcss": "^3.4.4",
    "vite": "^5.0.0"
  }
}
```

---

## 3. Estructura de Directorios

```txt
laravel-project/
├── app/
│   ├── Actions/                       # Acciones de negocio de responsabilidad única
│   ├── Enums/                         # Estados y roles tipados
│   ├── Livewire/                      # Componentes interactivos Livewire (Backend UI)
│   │   ├── Clientes/
│   │   │   ├── ListadoClientes.php
│   │   │   └── FormularioCliente.php
│   │   └── Dashboard/
│   │       └── GraficaVentas.php
│   ├── Models/                        # Modelos Eloquent en español
│   │   ├── Cliente.php
│   │   └── Proyecto.php
│   └── Services/                      # Integraciones con servicios y APIs externas
├── database/
│   ├── factories/                     # Fábricas de prueba
│   ├── migrations/                    # Migraciones declarativas
│   └── seeders/                       # Datos iniciales controlados
├── resources/
│   ├── css/app.css                    # Directivas Tailwind
│   ├── js/app.js                      # Inicialización de Alpine.js y ApexCharts
│   └── views/
│       ├── layouts/app.blade.php      # Layout maestro con scripts de Livewire y Alpine
│       ├── components/                # Componentes Blade reutilizables
│       └── livewire/                  # Vistas Blade vinculadas a componentes Livewire
├── routes/
│   └── web.php                        # Rutas web protegidas con middleware de auth
└── tests/
    └── Feature/                       # Pruebas funcionales con Pest
```

---

## 4. Reglas Técnicas y Convenciones
1. **Nombres en Español**: Modelos (`Cliente.php`, `Factura.php`), relaciones (`pedidos()`, `usuario()`), componentes Livewire (`FormularioContacto.php`) y vistas Blade en español.
2. **Reactividad Ligera con Alpine.js**: Usar Alpine para microinteracciones locales de UI (menús desplegables, modales, pestañas) y Livewire para mutaciones y llamadas al servidor.
3. **Gráficas con ApexCharts**: Inicializar componentes de ApexCharts mediante directivas de Alpine (`x-data="graficaApex(...)"`) consumiendo datos reactivos de Livewire.
4. **Pruebas con Pest**: Todo componente de Livewire y flujo crítico debe contar con pruebas en `tests/Feature/` verificando validaciones y estados de renderizado.
