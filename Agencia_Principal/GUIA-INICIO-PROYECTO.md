# Inicio de un proyecto

## 1. Identificar el trabajo
Usar el [asistente principal](asistente-principal.md). Acordar objetivo, criterios, alcance, ubicación del código y un ID exacto. La aplicación vive fuera de la carpeta de la agencia; conservar la estructura existente. Para trabajar desde otra carpeta usar rutas absolutas hacia los scripts de la agencia.

## 2. Elegir y registrar el perfil
Leer [stacks](stacks/README.md). El estándar se usa para proyectos nuevos sin otro perfil acordado; proyectos existentes conservan su tecnología. La creación registra contexto y memoria, no genera una aplicación ni provisiona infraestructura.

Desde la carpeta de la agencia:

```bash
python3 scripts/agencia.py doctor
python3 scripts/agencia.py nuevo cliente-web --cliente "Cliente" --stack estandar
python3 scripts/agencia.py arranque cliente-web --prime
```

Si el proyecto ya existe, no volver a crearlo. `doctor` distingue capacidades locales y conexiones pendientes; una herramienta opcional ausente no bloquea tareas que no la necesitan.

## 3. Preparar la implementación
Documentar requisitos y decisiones proporcionales al cambio. Resolver arquitectura en el manifiesto y perfil; asignar responsables y acordar contratos entre capas. Usar el árbol modular del frontend y los contratos backend/datos del perfil estándar cuando este sea el elegido. No copiar instalaciones TypeScript ni manifiestos de dependencias de otro perfil.

Para andamiaje, confirmar versiones compatibles y comandos oficiales del framework elegido en ese momento. Conservar versiones existentes. Un scaffolder puede instalar dependencias o ejecutar scripts: comprobar destino y alcance antes de usarlo. No inicializar Git, sobrescribir archivos o crear CI/despliegue si el proyecto ya los tiene o no los necesita.

## 4. Seleccionar skills y desarrollar
Consultar [selección de skills](reglas/seleccion-skills.md), leer fuentes pertinentes y comprobar entradas, herramientas y compatibilidad. No cargar todas ni fijar dependencias desde el rol.

```bash
python3 scripts/agencia.py skills --consulta frontend
python3 scripts/agencia.py skills --nombre frontend-modular
```

El asistente principal coordina frontend, backend y datos por dependencias reales. El orden puede cambiar según el trabajo; no imponer datos primero a una tarea visual ni pruebas de navegador a un servicio sin UI.

## 5. Verificar y cerrar
Ejecutar controles reales de la aplicación según sus criterios y riesgo. Documentar cambios, pruebas y pendientes sin afirmar migraciones o despliegues no ejecutados. Registrar cierre del proyecto cuando corresponde:

```bash
python3 scripts/agencia.py cierre cliente-web --tareas "Resultado comprobado" --decisiones "Decisión vigente" --pendientes "Control pendiente"
```

Para modificar la agencia, usar `verificar` y `comprobar`; esos controles no certifican el código de la aplicación. Publicación, contacto y operaciones sensibles requieren autorización concreta vigente. Audio y notificaciones son opcionales.

## Prompts de trabajo

Inicio: “Actúa según el asistente principal. Proyecto: <id>. Objetivo: <objetivo>. Alcance autorizado: <alcance>. Confirma el perfil y organiza el trabajo con criterios verificables.”

Reanudación: “Continúa el proyecto <id>. Recupera su contexto, verifica decisiones vigentes y ejecuta el siguiente paso dentro del alcance autorizado. Pregunta solo por lo imprescindible que falte.”

Cambio: “Implementa <resultado> en <id>, conserva contratos y convenciones existentes, selecciona skills pertinentes y entrega evidencia y pendientes.”

Cierre: “Revisa los criterios del alcance actual, ejecuta controles pertinentes y registra el resultado. No publiques ni despliegues por cerrar la revisión.”

## Cierre con evidencia

Para entregas sustanciales, completar `plantillas/entrega.json` con criterios y evidencias del proyecto y comprobar con `python3 scripts/agencia.py entregas evaluar informe.json --raiz-entrega /ruta/del/proyecto`. Código 0 indica completitud e integridad local; no autoriza publicar. Consultar los [escenarios operativos](contexts/agency/evaluacion-operativa.md) para evaluar agentes e integraciones según el trabajo realizado.

## Tareas y reanudación

Cuando una entrega requiera dependencias entre roles, adaptar `plantillas/plan-tareas.json` y registrarla con `agencia.py tareas crear <id> --plan plan.json`. Consultar la revisión actual al retomar; no iniciar dependientes hasta comprobar las entregas anteriores. El [control operativo](reglas/operacion-tareas.md) describe cierre, cancelación, nuevas fases e historial.
