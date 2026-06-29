# Flujo para Crear y Configurar un Proyecto Nuevo

## Objetivo
Establecer bases sólidas para un proyecto nuevo asegurando que su arquitectura, stack tecnológico y contexto inicial estén correctamente definidos desde el primer día.

## Pasos
1. **Entender el Requerimiento**: Comprender el dominio del negocio, el problema a resolver y los objetivos del proyecto. Revisa obligatoriamente los [Lineamientos de desarrollo](../reglas/lineamientos-desarrollo.md) antes de comenzar.
2. **Definir Stack y Arquitectura**: Aplicar el stack obligatorio de la agencia, acordar la estructura y los patrones, y documentar las excepciones aprobadas.
3. **Definir Perfil de Despliegue**: Si el proyecto tendrá Azure, ejecutar la fase de diseño de [desplegar-en-azure.md](desplegar-en-azure.md). Seleccionar servicios por requisitos, pero no crear recursos todavía.
4. **Inicializar Proyecto**:
   - Crear el repositorio o carpeta principal utilizando plantillas o frameworks base (`npx`, `vite`, etc.).
   - Inicializar el control de versiones (`git init`).
   - (Opcional) Ejecutar el script `scripts/nuevo_proyecto.py` para establecer la memoria del proyecto si se requiere integración nativa con la agencia.
5. **Configurar Entorno**: Añadir linters, formateadores de código (Ej. Prettier/ESLint), y frameworks de pruebas iniciales.
6. **Documentar el Contexto**: Crear o actualizar el `manifiesto-proyecto.md` detallando arquitectura de software, perfil de despliegue, variables y decisiones Azure aún no ejecutadas.
7. **Implementar el Núcleo (Core)**: Construir la base con contratos de puerto, salud, configuración, persistencia y migraciones compatibles con la decisión aprobada.
8. **Registrar Cierre Inicial**: Generar un informe de cierre de la fase de inicialización documentando tareas, dependencias base y próximos pasos.

## Criterio de cierre
La fase de inicialización se considera terminada cuando el proyecto compila/ejecuta exitosamente en su forma base, cuenta con documentación arquitectónica y perfil de despliegue en `context/`, y está listo para recibir desarrollo incremental. La infraestructura Azure puede seguir sin crear hasta la fase aprobada de entrega.
