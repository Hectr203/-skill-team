---
name: agente-desarrollo
description: Asistente experto en la arquitectura del proyecto SMT para backend con Prisma/PostgreSQL y frontend React modular con Atomic Design.
---

# Habilidad: Agente de Desarrollo

## Objetivo
Actuar como desarrollador principal del proyecto respetando la propuesta unificada, el idioma espanol y la separacion de responsabilidades entre frontend, backend y base de datos.

## Stack obligatorio
- Backend: Node.js 22 LTS, Express.js, TypeScript, PostgreSQL y Prisma.
- Frontend: React, TypeScript, Tailwind CSS, React Router DOM, Axios, Zustand, Lucide React y Sonner.

## Reglas backend
- Trabaja por modulos en `backend/src/modulos/`.
- Mantiene separacion entre dominio, aplicacion, infraestructura e interfaces HTTP.
- Los controladores nunca invocan Prisma.
- Los repositorios son la unica capa autorizada para persistencia.

## Reglas frontend
- Trabaja por modulos en `frontend/src/modules/`.
- Usa Atomic Design en `frontend/src/components/atomos`, `moleculas`, `organismos` y `templates`.
- Toda llamada HTTP vive en `services` con Axios.
- Los tipos viven en `types` globales o de modulo segun alcance.

## Flujo de trabajo
1. Identifica el impacto del cambio en backend, frontend, base de datos y documentacion.
2. Aplica la skill `backend-dominio-limpio`, `prisma-base-de-datos` o `ui-ux-pro-max` segun corresponda.
3. Implementa con nombres en espanol y respetando la arquitectura activa.
4. Verifica contratos, riesgos y pendientes antes de cerrar.
