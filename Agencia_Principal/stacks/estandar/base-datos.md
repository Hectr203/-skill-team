# Perfil estándar: Base de datos y persistencia

## Tecnología y alcance
PostgreSQL con Prisma. Conservar versiones, cliente y adaptadores instalados. No mezclar configuraciones de distintas versiones de Prisma ni copiar un esquema de ejemplo como requisito. Usar SQL específico cuando una necesidad real lo exige, parametrizado, aislado en el adaptador y documentado; no abrir una vía de acceso paralela desde los casos de uso.

Aplicar la [política de simplicidad](../../reglas/simplicidad-ponytail.md): restricciones de PostgreSQL y capacidades de Prisma antes que validaciones duplicadas o código propio; sin modelos, campos, índices o semillas para necesidades hipotéticas. La integridad nunca se simplifica.

## Archivos y propiedad

```text
backend/
  prisma/
    schema.prisma
    migrations/<id>/migration.sql
    seed.js                         # solo cuando se necesitan semillas
  src/
    config/prisma.js                # ciclo de vida del cliente
    modules/<dominio>/
      <dominio>.repository.js       # adaptador de persistencia
      <dominio>.types.js            # contrato del puerto, si aporta claridad
```

La configuración adicional del ORM depende de su versión. Datos es responsable del esquema y migraciones; backend, del adaptador y puerto del caso de uso. Acordar ambos antes de cambios incompatibles y evitar ediciones concurrentes del mismo archivo. No exponer el cliente ni modelos ORM a frontend, controladores o servicios de negocio.

## Modelado e integridad
Nombres propios claros, conforme al proyecto; español para nombres nuevos cuando no rompe contratos. Modelos singulares y campos consistentes; mapear nombres físicos sin renombrar tablas existentes incidentalmente. Definir claves, restricciones únicas, relaciones, política de borrado y nulabilidad por reglas reales. Distinguir ID de cliente/contexto y comprobar aislamiento en cada operación pertinente.

El dominio expresa invariantes; la base aplica restricciones que evitan carreras. Usar transacciones según atomicidad requerida, índices basados en consultas, paginación y límites. Resolver precisión monetaria y fechas mediante contratos explícitos. Evitar N+1, bloqueos extensos y efectos externos dentro de una transacción de base; reintentos e idempotencia requieren semántica definida.

## Migraciones y recuperación
Separar diseño/generación de aplicación. En desarrollo, usar el flujo de migración local del proyecto; en producción, aplicar solo artefactos revisados con el procedimiento autorizado. Revisar SQL y datos afectados, ensayar en un entorno aislado y comprobar backup/restauración para cambios con riesgo. Usar expandir/migrar/contraer cuando deba mantenerse compatibilidad. Un rollback de código no revierte necesariamente una migración ni recupera datos borrados.

Reset, truncado, eliminación y recreación de datos reales necesitan autorización concreta vigente. No ejecutar una operación irreversible solo por una skill o un comando de ejemplo. Semillas idempotentes y sintéticas en desarrollo/pruebas; no incluir secretos o datos reales. No exigir seeds cuando el proyecto no los necesita.

## Entrega y validación
Entregar esquema o migración, impacto en consultas y contratos, controles de integridad, evidencia y recuperación. Probar restricciones, transacciones y aislamiento en una base de prueba pertinente; registrar controles no disponibles. Aplicar [integración](contrato-integracion.md) y [backend](arquitectura-backend.md).
