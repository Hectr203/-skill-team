# Alternativas de Memoria para Agentes de IA

## Objetivo
Evaluar herramientas similares a CloudMem y Mem Palace para decidir si conviene integrarlas al flujo de Agentes Unificados.

## Alternativas revisadas

### Mem0 / OpenMemory
Mem0 ofrece una capa de memoria persistente para aplicaciones con LLM y tiene opcion open source/autohospedada. Es adecuada cuando se necesita busqueda semantica, integraciones con frameworks y control de infraestructura propia.

Ventajas:
- Puede autohospedarse.
- Tiene SDKs y enfoque de memoria persistente.
- Permite evolucionar hacia busqueda semantica.

Riesgos:
- Requiere configuracion adicional.
- Puede depender de LLMs, embeddings o vector stores externos.
- Para este proyecto documental, seria mas complejo que el beneficio inmediato.

### Letta / Letta Code
Letta esta orientado a agentes con estado persistente, memoria editable, mensajes almacenados y continuidad entre sesiones. Letta Code es atractivo para agentes de programacion que aprenden convenciones del repositorio.

Ventajas:
- Buen ajuste conceptual para agentes de desarrollo.
- Estado persistente por agente.
- Puede trabajar en modo local o con API.

Riesgos:
- Implica adoptar otra superficie de agente.
- No sustituye automaticamente la memoria local ya existente.
- Requiere flujo operativo adicional.

### Zep / Graphiti
Zep y Graphiti usan grafos temporales de contexto para registrar entidades, relaciones, hechos, historia y procedencia.

Ventajas:
- Muy potente para contexto cambiante y consultas historicas.
- Modela relaciones y temporalidad mejor que un log plano.
- Adecuado para produccion o multiples agentes con alto volumen.

Riesgos:
- Es mas pesado de operar.
- Requiere infraestructura adicional.
- No es necesario para el estado actual de Agentes Unificados.

## Recomendacion
Mantener Mem Palace como memoria estable y cifrada, y complementar con CloudMem local como historial operativo no sensible.

La alternativa externa mas conveniente para una evolucion futura es Mem0/OpenMemory, porque ofrece una ruta autohospedada y flexible sin obligar a cambiar completamente el modelo de agente. No se integra ahora porque el proyecto ya cuenta con Mem Palace funcional y la necesidad inmediata se cubre con scripts locales simples, auditables y sin dependencias nuevas.

## Decision actual
No se instala una dependencia externa por ahora.

Se implementa:
- Mem Palace acumulativo para decisiones y contexto estable.
- CloudMem local en `.cloudmem.jsonl` para historial operativo.
- Documentacion de arranque, consulta y cierre.

## Criterio para migrar en el futuro
Evaluar Mem0/OpenMemory si:
- El historial local crece demasiado.
- Se necesita busqueda semantica.
- Varios agentes deben consultar memoria por API.
- Se requiere integracion MCP o compatibilidad entre multiples herramientas de IA.
