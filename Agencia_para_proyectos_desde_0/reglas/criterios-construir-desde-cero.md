# Criterios para Construir desde Cero

## 1. Justificación de Construcción
Al iniciar un proyecto desde cero, tienes total libertad sobre la tecnología y la estructura, pero esto conlleva una gran responsabilidad. Todo código nuevo debe justificar su existencia mediante un requerimiento claro de negocio.

## 2. No Re-inventar la Rueda
Si existe una librería estándar, un framework o un paquete maduro que resuelva un problema común (como autenticación, validación de formularios o enrutamiento), úsalo en lugar de escribir código a medida desde cero.

## 3. Empezar Simple (MVP)
Prioriza construir el "Minimum Viable Product" (Producto Mínimo Viable). No pre-optimices ni construyas abstracciones excesivas que podrían no ser necesarias.
- "You Aren't Gonna Need It" (YAGNI): No implementes características que no se necesitan actualmente.
- "Keep It Simple, Stupid" (KISS): Mantén la solución lo más simple posible.

## 4. Evolución de la Arquitectura
La arquitectura debe estar diseñada para crecer. Las decisiones tempranas deben permitir adaptaciones futuras sin requerir una reescritura total.

## 5. Pruebas y Validaciones Frecuentes
A medida que se añade nuevo código, debe ser probado frecuentemente. La falta de código heredado significa que no hay dependencias problemáticas que impidan las pruebas, así que aprovecha esto desde el inicio.
