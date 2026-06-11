# Agencia Universal para Proyectos Existentes

## Proposito
Esta agencia esta disenada para continuar, mantener y mejorar proyectos que ya existen. Su regla principal es comprender primero el sistema actual y despues aplicar cambios pequenos, trazables y compatibles con la arquitectura, tecnologia, base de datos, reglas de negocio y convenciones ya definidas.

No impone un stack, framework, ORM, metodologia ni estructura de carpetas. Si el proyecto ya funciona con una arquitectura definida, los agentes deben conservarla salvo que exista una razon tecnica clara, documentada y validada para cambiarla.

## Estructura

```txt
Agencia_Proyectos_Existentes/
├── README.md
├── asistente-principal.md
├── agentes/
├── skills/
├── context/
├── guias/
├── flujos/
├── plantillas/
├── reglas/
├── proyectos/
├── scripts/
└── compatibilidad-ia/
```

## Carpetas principales

| Carpeta | Proposito |
| --- | --- |
| `agentes/` | Define roles especializados, responsabilidades, entradas, salidas, limites y criterios de uso. |
| `skills/` | Define habilidades reutilizables que pueden combinarse con agentes segun el tipo de tarea. |
| `context/` | Guarda guias para leer, resumir y conservar informacion del proyecto existente. |
| `guias/` | Explica como seleccionar agentes, skills y combinaciones recomendadas. |
| `flujos/` | Documenta flujos de trabajo para analizar, modificar, revisar, probar y cerrar cambios. |
| `plantillas/` | Incluye formatos base para nuevos agentes, nuevas skills, requerimientos, auditorias y bitacoras. |
| `reglas/` | Contiene reglas generales para preservar arquitectura, decidir cambios y evitar modificaciones innecesarias. |
| `proyectos/` | Contiene proyectos independientes, cada uno con su propia memoria contextual en `.memoria/`. |
| `scripts/` | Herramientas operativas de la agencia, incluida la memoria independiente por proyecto. |
| `compatibilidad-ia/` | Lineamientos para usar la agencia con Codex, Claude, Gemini, GitHub Copilot u otras IA. |

## Principios obligatorios
1. Leer antes de modificar.
2. Respetar la arquitectura existente.
3. Cambiar solo lo necesario para cumplir el objetivo.
4. Reutilizar patrones, nombres, carpetas, librerias y convenciones locales.
5. No instalar dependencias ni introducir frameworks sin justificacion.
6. Documentar decisiones que alteren arquitectura, base de datos, seguridad o reglas de negocio.
7. Validar con pruebas o verificacion manual segun el riesgo.
8. Mantener trazabilidad de archivos afectados, decisiones, riesgos y pendientes.

## Uso rapido
1. Inicia con [`asistente-principal.md`](asistente-principal.md).
2. Aplica [`context/lectura-proyecto-existente.md`](context/lectura-proyecto-existente.md) para entender el repositorio.
3. Selecciona agentes con [`guias/criterios-activacion-agentes.md`](guias/criterios-activacion-agentes.md).
4. Selecciona skills con [`guias/criterios-activacion-skills.md`](guias/criterios-activacion-skills.md).
5. Sigue el flujo apropiado en `flujos/`.
6. Cierra con documentacion usando las plantillas de `plantillas/`.

## Memoria por proyecto
Cada proyecto debe vivir en `proyectos/<nombre-proyecto>/` y tener memoria propia en `proyectos/<nombre-proyecto>/.memoria/`.

Para crear un proyecto desde la plantilla:

```bash
cp -R proyectos/_plantilla_proyecto proyectos/mi-proyecto
python3 scripts/memoria_proyecto.py --proyecto proyectos/mi-proyecto init
```

Antes de trabajar:

```bash
python3 scripts/memoria_proyecto.py --proyecto proyectos/mi-proyecto start
```

Despues de cambios importantes:

```bash
python3 scripts/memoria_proyecto.py --proyecto proyectos/mi-proyecto close \
  --tareas "Cambios realizados" \
  --pendientes "Pendientes" \
  --decisiones "Decisiones tecnicas" \
  --riesgos "Riesgos" \
  --cloud-resumen "Resumen operativo" \
  --archivos "archivo.md"
```
