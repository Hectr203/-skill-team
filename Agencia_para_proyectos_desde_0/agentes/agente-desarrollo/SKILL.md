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
1. Identifica el impacto del cambio en backend, frontend, base de datos, pruebas y documentacion.
2. Antes de escribir codigo, evalua si realmente hace falta con el principio YAGNI de `ponytail`.
3. Aplica la skill `backend-dominio-limpio`, `prisma-base-de-datos` o `ui-ux-pro-max` segun corresponda.
4. Implementa con nombres en espanol y respetando la arquitectura activa.
5. Escribe pruebas simultaneamente con la implementacion usando `playwright-mcp-testing`.
6. Verifica contratos, riesgos y pendientes antes de cerrar.
7. Ejecuta la bateria de pruebas localmente antes de marcar como completo.

## Anti-sobreingenieria
- No crees abstracciones que no se hayan solicitado explicitamente.
- No anadas dependencias que puedas evitar con la stdlib.
- No generes boilerplate que nadie pidio.
- Si una solucion existe en la stdlib o en una dependencia ya instalada, usala.
- Prefiere una linea sobre cinco. Prefiere un archivo sobre cinco.
- Marca simplificaciones intencionales con comentario `ponytail:`.
- Pregunta antes de abstraer: "realmente necesito esto o puedo resolverlo mas simple?"

## Pruebas como parte del desarrollo
- Escribe tests unitarios para toda logica pura (sin I/O).
- Escribe tests de integracion para endpoints de API.
- Escribe tests E2E solo para flujos criticos de usuario.
- Usa Playwright para todo: unitario, integracion y E2E.
- Sigue TDD (Red-Green-Refactor) para bugs y funcionalidades nuevas.
