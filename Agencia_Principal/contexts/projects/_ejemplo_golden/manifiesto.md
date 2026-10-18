# Piloto de referencia de la agencia

- ID: _ejemplo_golden
- Cliente y marca: ejemplo ficticio, sin datos de clientes.
- Tipo: auditoria
- Objetivo: comprobar el ciclo local de creación, arranque, cierre y recuperación.
- Stack Tecnológico Asignado: stacks/estandar
- Alcance: CLI, MCP y memoria. No certifica una aplicación desplegada.
- Historia de usuario: como operador, quiero reanudar un proyecto sin mezclar su memoria con la de otro cliente.
- Criterios de aceptación: dos IDs producen memorias independientes; el cierre aparece en el siguiente arranque y en MCP; fallos operativos se comunican como errores.
- Casos de prueba: `tests/test_flujo_piloto.py` y `tests/test_controles.py`.
- Comando: `python3 -m unittest discover -s tests -v` desde la raíz de la agencia.
- Evidencia: salida real del comando; no considerar la mera presencia de esta ficha como prueba aprobada.
- Fuera de alcance: credenciales externas, despliegue, ventas y rentabilidad.
