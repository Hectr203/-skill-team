# Reglas de Creación de Arquitectura

## Principio General
La arquitectura debe servir al producto, no al revés. No compliques excesivamente un proyecto nuevo sin justificación basada en los requerimientos.

## Directrices
1. **Definir Antes de Construir**: Antes de escribir el primer archivo de lógica, se debe definir y documentar la arquitectura principal (monolito, microservicios, capas, MVC, etc.).
2. **Convenciones Claras**: Establecer desde el inicio las convenciones de nombres (camelCase, snake_case), organización de carpetas y manejo de estado.
3. **Escalabilidad Gradual**: Comienza con una arquitectura simple que pueda evolucionar. No implementes infraestructuras hiper-complejas (como Kubernetes o CQRS) para un MVP a menos que sea un requerimiento explícito.
4. **Documentación Activa**: Toda decisión arquitectónica debe ser registrada en el contexto del proyecto para servir de guía durante el desarrollo incremental.
5. **Independencia de Componentes**: Promover bajo acoplamiento y alta cohesión desde las primeras líneas de código.
