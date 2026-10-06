# Proyectos Gestionados — Agencia Principal

Este directorio contiene los espacios de trabajo, memoria estructurada y trazabilidad técnica de todos los proyectos desarrollados o auditados por la **Agencia Principal**.

---

## 1. Estructura de Proyectos

Cada proyecto vive en su propio subdirectorio bajo `contexts/projects/<nombre_proyecto>/`:

```txt
contexts/projects/<nombre_proyecto>/
├── manifiesto.md              # Contrato maestro del proyecto, alcance y stack asignado
├── memoria.md                 # Resumen operativo de continuidad entre sesiones
├── .memoria/                  # Almacén estructurado: .cloudmem.jsonl, mem_palace.enc, key
├── adrs/                      # Decisiones de Arquitectura (ADR-001-<nombre>.md)
└── evidencias/                # Capturas, recibos de testing y reportes de QA
```

---

## 2. Proyectos Especiales del Sistema

1. **`_plantilla_proyecto/`**:
   - Plantilla base que el comando `python3 scripts/agencia.py nuevo <nombre>` utiliza para inicializar proyectos nuevos sin errores de estructura.
2. **`_ejemplo_golden/`**:
   - Proyecto de referencia completo con ADRs reales, memoria inicializada y evidencias de prueba. Sirve como estándar de calidad (Benchmark) para validar el comportamiento de los agentes.

---

## 3. Comandos Útiles

```bash
# Ver estado de todos los proyectos registrados
python3 scripts/agencia.py estado

# Inicializar un nuevo proyecto
python3 scripts/agencia.py nuevo mi-proyecto --cliente "Acme Corp" --stack estandar

# Cargar contexto para un LLM (--prime genera System Primer conciso)
python3 scripts/agencia.py arranque mi-proyecto --prime
```
