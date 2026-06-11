# Pendientes de validacion

## Resumen

Estos puntos deben resolverse antes de cerrar el levantamiento de requerimientos o iniciar cambios irreversibles de base de datos, permisos o arquitectura.

## Pendientes criticos

### PV-01 Responsable real de altas de unidades

Decision pendiente:

- Confirmar si existe una persona encargada de administrar todas las unidades nuevas.
- Confirmar si Daniela, otra persona o un area especifica asumira ese rol.

Regla temporal:

- Se usara `administrador_global` como unico responsable de altas hasta nueva validacion.

Impacto:

- Afecta permisos, flujo de alta, auditoria y diseno de roles.

### PV-02 Roles existentes de Angel y Roberto

Decision pendiente:

- Recibir scripts, capturas o archivos de roles actuales.
- Confirmar si sus aplicaciones tienen tabla de usuarios, roles o permisos.

Impacto:

- Afecta migracion de usuarios, compatibilidad con aplicaciones actuales y permisos iniciales.

### PV-03 Campos obligatorios de unidad

Decision pendiente:

- Confirmar si los campos base detectados en `SMT Parque Vehicular.xlsx` son suficientes para el alta inicial.
- Separar campos administrativos, operativos, documentales, de cumplimiento y de calculo.

Campos base detectados:

- Numero de unidad.
- Numero economico, cuando aplique.
- Marca.
- Tipo.
- Serie.
- Motor.
- Placas.
- Factura.
- T/C o tarjeta de circulacion.
- Numero de poliza.
- Vigencia.

Campos complementarios y por validar:

- Modelo o anio modelo.
- Color.
- Verificacion.
- Contaminantes.
- Fisico-mecanica.
- Costo.
- Odometro inicial.
- Area o categoria.
- Operadores asignables.
- Capacidad.
- Tarifa base.
- Sueldo de operador.
- Rendimiento regular.
- Rendimiento bajo.
- Numero de ejes.

Impacto:

- Afecta modelo de dominio, validaciones y formularios.
- Afecta la estrategia de importacion del Excel, porque existen fechas como numeros seriales, valores vacios, `NO TIENE`, `EXCENTO` y registros incompletos.

### PV-04 Reglas exactas de mantenimiento

Decision pendiente:

- Confirmar si los mantenimientos se programan cada 30 dias, por kilometraje, por piezas o por reglas combinadas.
- Confirmar si las alertas de 30, 15 y 3 dias son obligatorias para todos los mantenimientos.
- Confirmar si se requiere alerta por vencimiento de seguro o documentos.

Impacto:

- Afecta calculo de alertas, notificaciones y consultas prioritarias.

### PV-05 Categorias y areas definitivas

Decision pendiente:

- Confirmar si las cinco categorias iniciales son definitivas: ATAH, Oaxaca, turismo, tracto y transporte de personal.
- Confirmar si fletes sera categoria, area consumidora, aplicacion o subclasificacion de tracto.
- Confirmar si cotizaciones es area operativa o modulo dentro de turismo.

Impacto:

- Afecta filtros, permisos, reportes y reasignaciones.

### PV-06 Token central y logins existentes

Decision pendiente:

- Confirmar si las aplicaciones reemplazaran su login local con el login central.
- Confirmar si habra convivencia temporal de token local mas token central.
- Confirmar si cada backend consumidor validara el token llamando a la API o verificara JWT localmente.

Impacto:

- Afecta seguridad, integracion y migracion de aplicaciones existentes.

### PV-07 Datos visibles por rol

Decision pendiente:

- Definir que campos puede ver cada rol o aplicacion.
- Confirmar si datos como sueldo de operador, polizas o documentos deben ocultarse para ciertos perfiles.

Impacto:

- Afecta DTOs de salida, permisos y privacidad.

### PV-08 Operadores asignables

Decision pendiente:

- Confirmar si operadores se administraran dentro de la API central o en otro sistema.
- Confirmar si una unidad puede tener uno o varios operadores asignables.

Impacto:

- Afecta modelo de dominio y relaciones futuras.

### PV-09 Importacion desde Excel o tablas existentes

Decision pendiente:

- Confirmar si se migraran datos actuales desde Excel o bases existentes.
- Obtener archivos, scripts o exportaciones.
- Definir limpieza de duplicados antes de importar.

Impacto:

- Afecta semillas, migraciones, validaciones y pruebas de integridad.

### PV-10 Alcance de reportes personalizados

Decision pendiente:

- Confirmar que reportes necesita cada area.
- Confirmar frecuencia, formato y destinatarios.

Impacto:

- Afecta endpoints, filtros y posibles vistas frontend.

## Pendientes por responsable

### Angel

- Compartir roles existentes de su aplicacion.
- Confirmar informacion exacta que requiere taller.
- Confirmar estados usados actualmente para unidades en taller.

### Roberto

- Compartir roles existentes de su aplicacion.
- Confirmar campos de calculo: capacidad, tarifa base, sueldo, rendimientos y numero de ejes.
- Confirmar categorias que debe consultar: turismo, Oaxaca u otras.

### Daniela o responsable por confirmar

- Confirmar si administra altas de unidades nuevas.
- Confirmar si solo consulta catalogo o tambien edita unidades.
- Confirmar reglas para unidades nuevas, descompuestas o dadas de baja.

### Humano responsable del proyecto

- Validar estos documentos.
- Aprobar pasar del ciclo documental al Sprint 1 tecnico.
- Aprobar cambios de base de datos y seguridad antes de implementarlos.

## Riesgos si no se validan

- Duplicidad de unidades entre aplicaciones.
- Permisos incorrectos o exposicion de datos privados.
- Modelo de base de datos incompleto o dificil de migrar.
- Aplicaciones existentes incompatibles con la API central.
- Reglas de mantenimiento incorrectas.
- Confusion entre categoria, area, modulo y estado operativo.

## Recomendacion de siguiente accion

Revisar esta carpeta con Angel, Roberto y el responsable de altas. Despues convertir los pendientes cerrados en tareas tecnicas para Sprint 1.
