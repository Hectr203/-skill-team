# Verificación local de cambios

La agencia utiliza Python y su propia suite para comprobar el contenido local.

## Después de aplicar cambios

Ejecutar desde la raíz de la agencia:

```bash
python3 scripts/agencia.py verificar
```

El comando ejecuta el validador y las pruebas. Guarda códigos de salida,
resultados y huellas SHA-256 en `.agencia/verificacion-local.json`.
Si los archivos cambian durante las comprobaciones o alguna falla,
el informe queda marcado como fallido.

## Antes de confirmar, subir o publicar

```bash
python3 scripts/agencia.py comprobar
```

Esta comprobación no repite pruebas: exige un informe aprobado y el mismo
contenido. Altas, bajas y modificaciones invalidan el resultado.
Continuar únicamente con código 0. Después de corregir un fallo o cambiar
archivos, ejecutar `verificar` otra vez de forma explícita.

El alcance es la agencia de este checkout, no la aplicación de otro directorio.
Para publicar una revisión Git, comprobar que el índice o la revisión candidata
contengan exactamente los archivos verificados; este comando no instala hooks
ni certifica automáticamente el índice, commits remotos o producción.

El informe excluye cachés, dependencias instaladas, compilados, evidencias,
memoria privada y claves. No demuestra ausencia de problemas en esas áreas.
No modifica Git, usa cuentas externas ni concede autorización para publicar.

Las pruebas no equivalen a una revisión humana de diseño o seguridad.
Ante cambios sensibles, documentar riesgos y revisión proporcional al cambio.
El informe es evidencia local reproducible, no una firma contra manipulación
por alguien con acceso al mismo equipo.
