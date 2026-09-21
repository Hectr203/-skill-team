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
