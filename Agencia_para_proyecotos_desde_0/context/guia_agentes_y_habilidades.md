# Guia de Agentes y Habilidades de la Agencia SMT

Esta guia resume como deben operar los agentes y skills de la agencia SMT. La referencia tecnica principal es [propuesta_unificada.md](/mnt/nvme/repo%20smt%20para%20desarollo/Agentes_Unificados/context/propuesta_unificada.md).

## 1. Agentes principales

### `asistente-principal`
- Punto de entrada obligatorio con el humano.
- Clasifica la tarea, hace preguntas, define alcance, selecciona metodologia, agentes y skills.
- Decide entre Cloud Mem y Mem Palace segun sensibilidad de la tarea.

### `agente-desarrollo`
- Implementa backend, frontend e integraciones respetando la arquitectura global.
- Debe apoyarse en `backend-dominio-limpio`, `prisma-base-de-datos` y `ui-ux-pro-max` segun la capa afectada.

### `agente-backend`
- Mantiene APIs y casos de uso con Node.js 22 LTS, Express.js, TypeScript, PostgreSQL y Prisma.
- Debe evitar Prisma fuera de repositorios y respetar Clean Architecture.

### `agente-frontend`
- Mantiene componentes base y modulos React con Tailwind CSS, Axios, Zustand, Sonner y Lucide React.
- Debe respetar Atomic Design en `atomos`, `moleculas`, `organismos` y `templates`.

### `agente-base-de-datos`
- Disena `schema.prisma`, migraciones, semillas y repositorios bajo PostgreSQL y Prisma.
- Debe proteger integridad referencial y evitar SQL crudo innecesario.

### `ingeniero-de-pruebas`
- Valida historias de usuario, criterios de aceptacion, casos de uso, riesgos y regresiones.

### `revisor-de-codigo`
- Revisa correctitud, legibilidad, arquitectura, seguridad y rendimiento antes del cierre.

### `auditor-de-seguridad`
- Audita entradas, autenticacion, autorizacion, secretos, integraciones y fronteras del sistema.

## 2. Skills tecnicas obligatorias

### `backend-dominio-limpio`
- Aplica a endpoints, casos de uso, servicios, controladores y repositorios backend.
- Refuerza Clean Architecture, dominio limpio y arquitectura hexagonal.

### `prisma-base-de-datos`
- Aplica a modelos Prisma, migraciones, semillas, transacciones y acceso a datos.
- Refuerza PostgreSQL como motor definitivo y Prisma como ORM obligatorio.

### `ui-ux-pro-max`
- Aplica a diseno visual, experiencia de usuario, accesibilidad y componentes frontend.

### `ahorro-contexto`
- Aplica al arranque y cierre de sesion, memoria persistente y lectura eficiente del repositorio.

### `commits-espanol`
- Aplica a commits, reportes de cambios y trazabilidad documental.

## 3. Skills de negocio SMT

### `administrador-equipos-moviles-transporte`
- Ayuda a razonar mantenimiento, combustible, capacidad de unidades y operacion de flota.

### `conductor-transporte-personal`
- Ayuda a disenar flujos seguros y simples para choferes con baja friccion operativa.

### `experto-logistica-transporte-personal`
- Ayuda a razonar rutas, contingencias y reglas operativas del negocio.

## 4. Reglas transversales

- Todo el proyecto se mantiene en espanol, salvo sintaxis, palabras reservadas y nombres inevitables de frameworks o librerias.
- Backend obligatorio: Node.js 22 LTS, Express.js, TypeScript, PostgreSQL y Prisma.
- Frontend obligatorio: React, TypeScript, Tailwind CSS, Lucide React, Sonner, Zustand, Axios y React Router DOM.
- Quedan prohibidos `SQL Server`, `Knex` y `TanStack Query` como base tecnica del proyecto, salvo excepcion aprobada y documentada.
- Toda coordinacion entre agentes pasa por el asistente principal.
- El humano debe validar alcance, cambios sensibles, entregables y excepciones tecnicas.

## 5. Memoria persistente

- Usa Cloud Mem para tareas visuales, agiles y no sensibles de frontend.
- Usa Mem Palace para backend, base de datos, Prisma, reglas de negocio, seguridad y decisiones tecnicas criticas.
- Si una tarea mezcla frontend con backend, separa el contexto por sensibilidad.
- Si existe duda, prioriza Mem Palace.

## 6. Seleccion rapida

1. Si la tarea es ambigua, inicia con `asistente-principal` y, si hace falta, `analista-requerimientos`.
2. Si toca backend, usa `agente-desarrollo` o `agente-backend` con `backend-dominio-limpio`.
3. Si toca base de datos, suma `agente-base-de-datos` con `prisma-base-de-datos`.
4. Si toca interfaz, usa `agente-frontend` con `ui-ux-pro-max`.
5. Si el cambio es critico, incorpora `ingeniero-de-pruebas`, `revisor-de-codigo` o `auditor-de-seguridad` segun riesgo.
