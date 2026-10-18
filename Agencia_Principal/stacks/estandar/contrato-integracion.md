# Contrato de integración del perfil estándar

## Lectura de entrada
El manifiesto identifica perfil y estado real de frontend, backend y datos. Leer las tres entradas del perfil, la arquitectura de la capa afectada y ADRs relevantes antes de implementar. Si lo existente difiere, registrar la diferencia y mejorar solo el alcance autorizado. No afirmar que este contrato ha sido aplicado al código por existir la documentación.

## Responsables y traspasos
- Frontend: módulos, UI y consumo del contrato API; no cambia esquema o autorización del servidor.
- Backend: contrato API, casos de uso y adaptadores; acuerda cambios de persistencia con datos.
- Datos: esquema, migraciones e integridad; informa a backend compatibilidad, índices y recuperación.

Cada artefacto tiene un dueño. Un traspaso incluye objetivo, archivo, contrato, evidencia, dependencias y criterio pendiente; no solicita al receptor redescubrir toda la tarea. La coordinación ocurre según el [contrato común de agentes](../../agentes/contrato-agente.md), sin creación automática de procesos.

## Contrato API compartido
Acordar método/ruta, entradas, resultado, errores, permisos y contexto de cliente. Precisar paginación, fechas, moneda, nulabilidad y semántica de reintentos cuando aplica. El DTO público es independiente del modelo ORM. Mantener contrato documentado en la ubicación real del proyecto —por ejemplo OpenAPI o documentación existente—; no imponer una segunda fuente duplicada.

## Validación de cambios
Frontend prueba flujos y estados; backend prueba casos de uso y contratos; datos prueba restricciones, migraciones y aislamiento. Verificar recorridos entre capas para cambios que atraviesan API y persistencia. Las pruebas se ajustan al riesgo y los comandos disponibles. Una validación local de la agencia no acredita estos controles sobre la aplicación.
