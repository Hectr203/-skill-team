# Plantilla de Proyecto

Usa esta carpeta como base para agregar un nuevo proyecto dentro de `Agentes_Unificados/proyectos/`.

## Crear nuevo proyecto

```bash
cp -R proyectos/_plantilla_proyecto proyectos/mi-proyecto
python3 skills/ahorro-contexto/scripts/memoria_proyecto.py --proyecto proyectos/mi-proyecto init
```

## Regla
Cada proyecto debe tener memoria propia en `.memoria/`. No se debe usar la memoria raiz de la agencia como memoria compartida de proyectos.
