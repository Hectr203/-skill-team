# Referencia de contexto de proyecto

Esta carpeta conserva ejemplos de contexto. El comando de creación utiliza las plantillas de `plantillas/`; no copia este directorio.

Desde la raíz de la agencia:

```bash
python3 scripts/agencia.py nuevo mi-proyecto --cliente "Cliente"
python3 scripts/agencia.py arranque mi-proyecto --prime
```

Cada proyecto mantiene su manifiesto, memoria y decisiones en `contexts/projects/<id>/`. No compartir memoria entre clientes. La aplicación se desarrolla en su propio repositorio.
