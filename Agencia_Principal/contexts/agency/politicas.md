# Políticas operativas

Aplicar [precedencia](../../reglas/precedencia.md), [aislamiento](../../reglas/aislamiento-contexto.md)
y [aprobación humana](../../reglas/human-in-the-loop.md).

- Secretos en el gestor del entorno; nunca en prompts, configuraciones versionables ni memoria.
- Identidad explícita de cliente/proyecto. No inferirla a partir del nombre de una carpeta externa.
- Markdown y JSONL son legibles; minimizar información personal y confidencial.
- La clave de cifrado local se crea con permisos restringidos; no compartirla con el historial público.
- Copias de seguridad y recuperación se acuerdan por proyecto. Documentar responsables, periodicidad, destino y una prueba de restauración; no asumir que Git protege archivos ignorados.
- Retención, eliminación y publicación de datos requieren el acuerdo concreto del cliente y una decisión del operador. No inventar plazos legales o contractuales.
- Antes de publicar: comprobar secretos, pruebas y permisos; aplicar la [verificación local](../../reglas/verificacion-local.md) al contenido candidato y documentar la revisión de cambios sensibles.
- Una prueba local aprobada no equivale a un despliegue aprobado ni a una conexión externa verificada.
