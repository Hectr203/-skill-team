# Agencia Principal — Sistema Integral de Agentes de IA

Bienvenido a la **Agencia Principal**, el ecosistema unificado y de nivel industrial para desarrollo de software guiado por especificaciones (Spec-Driven Development), orquestación multi-agente, aseguramiento de calidad (QA) y gestión integral de proyectos digitales.

> 📖 **¿Iniciando un proyecto desde cero en un nuevo repositorio?**
> Consulta la **[Guía Maestra de Inicio y Desarrollo de Proyectos](GUIA-INICIO-PROYECTO.md)** con la estructura de carpetas recomendada, el flujo en 5 pasos y los prompts exactos para copiar y pegar en el chat de tu IA.

---

## 🚀 Inicio Rápido con el CLI Operativo

La agencia cuenta con una interfaz de línea de comandos centralizada en `scripts/agencia.py` y un servidor MCP nativo en `scripts/agencia_mcp.py`:

```bash
# 1. Diagnosticar el entorno operativo y herramientas
python3 scripts/agencia.py doctor

# 2. Validar la integridad estructural completa de la agencia (agentes, skills, scripts)
python3 scripts/agencia.py validar

# 3. Ver el estado y dashboard de todos los proyectos gestionados
python3 scripts/agencia.py estado

# 4. Crear un nuevo proyecto con el stack estándar (Node 22 + React + Prisma)
python3 scripts/agencia.py nuevo mi-proyecto-web --cliente "Cliente Demo"

# 5. Crear un nuevo proyecto con un stack alternativo (ej. Laravel Livewire Alpine)
python3 scripts/agencia.py nuevo mi-proyecto-laravel --stack laravel-livewire-alpine

# 6. Iniciar sesión de trabajo y cargar contexto optimizado en tokens (--prime)
python3 scripts/agencia.py arranque mi-proyecto-web --prime

# 7. Registrar cierre de sesión con trazabilidad y alerta sonora
python3 scripts/agencia.py cierre mi-proyecto-web --tareas "Endpoints implementados" --notificar
```

---

## 🏛️ Arquitectura del Repositorio

```txt
Agencia_Principal/
├── opencode.json                  # Integración de skills y MCP para OpenCode / Antigravity
├── AGENTS.md                      # Reglas globales inmutables, español mandatorio y FinOps
├── asistente-principal.md         # Orquestador supremo, loops SDD-QA y compuertas HITL
│
├── agentes/                       # 16 Agentes Especializados de ingeniería y dominios
│   ├── agente-orquestador.md      # Asistente Principal y Coordinador
│   ├── analista-requerimientos.md # Levantamiento de requerimientos formales, HU y CA
│   ├── agente-arquitectura.md     # Arquitectura hexagonal, modular y ADRs
│   ├── agente-backend.md          # Node 22, Express, TS, Prisma, Clean Architecture (+500 líneas)
│   ├── agente-frontend.md         # React, TS, Tailwind, Atomic Design, Sonner, Zustand
│   ├── agente-base-datos.md       # PostgreSQL, esquemas Prisma, migraciones aditivas
│   ├── ingeniero-de-pruebas.md    # Playwright E2E, pruebas unitarias/integración, reportes QA
│   ├── revisor-de-codigo.md       # Code review estricto, linters y mantenibilidad
│   ├── auditor-seguridad.md       # Threat modeling, OWASP, secretos y permisos
│   ├── agente-despliegue-azure.md # Azure CLI, App Services, Functions, Docker, CI/CD
│   ├── agente-documentacion.md    # Trazabilidad técnica, bitácoras y actas de cierre
│   ├── agente-contexto.md         # Memoria persistente, compresión y continuidad
│   ├── diseno-motion.md           # Google Stitch, React Bits, Anime.js, tokens
│   ├── seo-tecnico.md             # SEO técnico, GEO AI optimization, Schema Markup
│   ├── crm-leads.md               # Auto-CRM SQLite, embudos de venta, webhooks
│   ├── redes-sociales.md          # Voice builder, LinkedIn, guiones para reels
│   ├── contrato-agente.md         # Plantilla contractual de entradas, salidas y límites
│   └── guia-de-personas.md        # Estilos de comunicación y personalidades
│
├── context/                       # Documentación Maestra y Gobernanza
│   ├── propuesta_unificada.md     # Gobernanza técnica obligatoria
│   ├── propuesta_estructura.md    # Arquitectura de proyectos de software reutilizable
│   ├── guia_agentes_y_skills.md   # Matriz de asignación y responsabilidades
│   ├── flujo_memoria.md           # Protocolo de 3 capas de memoria persistente
│   └── alternativas_memoria.md    # Análisis y justificación de persistencia
│
├── stacks/                        # Arquitectura Multi-Stack Modular y Auto-Adaptable
│   ├── README.md                  # Guía del sistema multi-stack, resolución y herencia
│   ├── estandar/                  # Stack Predeterminado Oficial (Node 22 / Express / TS / Prisma / React)
│   ├── plantillas/                # Plantilla base para registrar nuevos stacks tecnológicos
│   └── alternativos/              # Perfiles tecnológicos adicionales (Laravel/Livewire/Alpine, etc.)
│
├── contexts/                      # Contextos Operativos Vivos
│   ├── projects/                  # Directorio de proyectos (_plantilla_proyecto y _ejemplo_golden)
│   ├── clients/                   # Documentación estructurada por cliente
│   ├── brands/                    # Guías de voz y tono de marca
│   ├── campaigns/                 # Registro y seguimiento de campañas activas
│   └── agency/                    # Acuerdos internos, tarifas y capacidades
│
├── flujos/                        # 12 Flujos de Trabajo Guiados Paso a Paso
├── reglas/                        # Reglas y Estándares de Ingeniería
├── scripts/                       # Motor Operativo Unificado y Servidor MCP
├── audios/                        # Audios Oficiales de Alerta Local (4 archivos .mp3)
├── skills/                        # Habilidades Reales (Completas y Descubribles)
└── tests/                         # Suite de Pruebas Automatizadas
```

---

## 🎯 Pilares Diferenciadores

1. **Ahorro Extremo de Tokens y Navegación Basada en Grafos**:
   - Queda prohibida la búsqueda ciega con `grep`/`find`.
   - Se consulta obligatoriamente **CodeGraph** para exploración de código/símbolos y **Graphify** para mapas conceptuales.
   - Salidas extensas se comprimen con **Headroom** hasta un 80%.
2. **Sistema Multi-Stack Auto-Adaptable**:
   - Stack estándar predeterminado e inmutable en `stacks/estandar/`.
   - Capacidad dinámica de crear perfiles alternativos en `stacks/alternativos/` ante nuevas tecnologías sin romper la estandarización habitual.
3. **Compuertas Human-in-the-Loop Auditadas**:
   - Avisos audibles locales reproducidos exactamente 2 veces (`termine la tarea.mp3`, `Necesito Validación.mp3`, `Aprobación urgente..mp3`).
   - Trazabilidad con registro auditado en `.hitl_audit.jsonl`.
4. **Ciclo de Iteraciones SDD y QA**:
   - Límite de 5 loops de corrección entre QA y Desarrollo.
   - Cierre exclusivo por evidencia de pruebas verificables en verde.
