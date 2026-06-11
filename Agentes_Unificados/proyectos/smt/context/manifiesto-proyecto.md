# Manifiesto del Proyecto SMT

## Proposito

Este documento identifica a SMT como un proyecto especifico de la agencia y define que contexto, agentes y skills deben cargarse cuando el trabajo pertenezca a este dominio.

## Campos recomendados

- nombre del proyecto
- dominio o rubro
- descripcion corta del negocio
- stack tecnico del proyecto
- skills especificas habilitadas
- agentes especificos habilitados
- restricciones de seguridad
- reglas de memoria persistente
- documentos de contexto obligatorios

## Memoria persistente del proyecto

- Ruta de memoria: `Agentes_Unificados/proyectos/smt/.memoria/`
- Consulta: `python3 skills/ahorro-contexto/scripts/arranque.py --proyecto proyectos/smt`
- Cierre: `python3 skills/ahorro-contexto/scripts/cierre.py --proyecto proyectos/smt ...`
- Regla: la memoria de SMT no debe mezclarse con otros proyectos ni con la memoria raiz general de la agencia.

## Uso esperado

El asistente principal debe leer este manifiesto para decidir:

1. si la tarea pertenece a SMT
2. que skills especificas debe importar
3. que agentes de proyecto debe activar
4. que contexto no debe contaminar otros proyectos
5. que memoria independiente debe consultar y actualizar
