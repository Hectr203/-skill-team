# Reglas generales de trabajo

Aplicar [precedencia](precedencia.md) y el [asistente principal](../asistente-principal.md).

- Todo cambio responde al objetivo autorizado y conserva contratos fuera de su alcance.
- Aplicar obligatoriamente Ponytail para evitar la sobreingeniería. En desarrollo y revisión (backend, persistencia y frontend) rige la [política de simplicidad](simplicidad-ponytail.md) en nivel `full`; solo el asistente principal o el usuario cambian el nivel. Ninguna regla obliga a crear capas, patrones, dependencias o archivos sin justificación técnica concreta. Justificar simplificaciones con límite conocido mediante `// ponytail:`.
- Revisar contexto y código real antes de crear archivos, dependencias o abstracciones. Preferir la solución sencilla que preserve seguridad y comportamiento.
- El manifiesto y perfil definen arquitectura; las skills complementan la ejecución mediante [selección](seleccion-skills.md).
- Analizar compatibilidad y recuperación de datos antes de migraciones. Operaciones sensibles siguen [HITL](human-in-the-loop.md).
- Planificar y documentar proporcionalmente al cambio; conservar decisiones estables en la ubicación acordada. No imponer rutas de un IDE ni crear informes redundantes.
- Verificar criterios con controles pertinentes, informar fallos y no repetir una corrección fallida sin cambiar el enfoque.
- La entrega distingue completado, parcial y bloqueado, con evidencia y próximos responsables.
