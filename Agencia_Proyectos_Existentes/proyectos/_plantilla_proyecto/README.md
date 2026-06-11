# Plantilla de Proyecto Existente

Esta carpeta sirve como base para iniciar un nuevo proyecto dentro de la Agencia Universal para Proyectos Existentes.

## Crear un nuevo proyecto (método recomendado)

Desde la raíz de la agencia, ejecuta un solo comando:

```bash
python3 scripts/nuevo_proyecto.py <nombre-proyecto>
```

El script copia esta plantilla y genera automáticamente la memoria independiente del nuevo proyecto.

## Método manual

Si prefieres hacerlo paso a paso desde la raíz de la agencia:

```bash
cp -R proyectos/_plantilla_proyecto proyectos/<nombre>
python3 scripts/memoria_proyecto.py --proyecto proyectos/<nombre> init
```

## Siguientes pasos después de crear el proyecto

1. Completa `context/manifiesto-proyecto.md` con el nombre, propósito y tecnologías del proyecto.
2. Consulta la memoria al inicio de cada sesión:
   ```bash
   python3 scripts/arranque.py --proyecto proyectos/<nombre>
   ```
3. Registra el cierre después de cada cambio importante:
   ```bash
   python3 scripts/cierre.py --proyecto proyectos/<nombre> \
     --tareas "Primera sesion de contexto" \
     --cloud-resumen "Proyecto inicializado"
   ```

## Regla
La carpeta `.memoria/` pertenece solo a este proyecto. No debe reutilizarse ni copiarse hacia otros proyectos.
