# Aislamiento de contexto

```text
contexts/
├── agency/
├── projects/<project-id>/
├── clients/<client-id>/
├── brands/<brand-id>/
└── campaigns/<campaign-id>/
```

Un agente recibe solo el contexto mínimo de su dominio. No mezclar clientes,
marcas, keywords, leads, contratos ni memoria. `voice.md` solo aplica a su
marca. Secretos viven fuera de Markdown, preferiblemente en el gestor del
entorno o `.env` ignorado. Los exports de memoria son concisos, versionables y
sin secretos.

Cada proyecto utiliza un ID único y explícito, preferiblemente `<cliente>-<proyecto>`.
Los scripts aceptan ese ID o su ruta exacta dentro de `contexts/projects/`.
Una ruta externa, un ID vacío o un enlace simbólico se rechaza; no se deduce
la identidad por el último nombre de carpeta. Los proyectos existentes
conservan su ID y su historial. Si se necesita renombrarlos,
planificar y verificar la migración antes de mover memoria.
