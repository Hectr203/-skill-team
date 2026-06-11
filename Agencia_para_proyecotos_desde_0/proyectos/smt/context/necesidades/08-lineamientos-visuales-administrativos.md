# Lineamientos visuales administrativos

## Resumen

La interfaz administrativa de SMT debe tomar como base las referencias visuales proporcionadas en:

- `context/eslilos visuales ejemplos/Screenshot_2026-06-09-22-34-32-511_com.google.android.gm.jpg`
- `context/eslilos visuales ejemplos/Screenshot_2026-06-09-22-38-22-222_com.google.android.gm.jpg`

Estas referencias muestran un patron claro: panel administrativo con barra lateral oscura, encabezado superior sobrio, contenido principal luminoso, acentos rojos y componentes centrados en lectura, supervision y accion.

## Direccion visual

El frontend no debe verse como una plantilla generica ni como un dashboard plano. Debe sentirse como una consola administrativa profesional para operacion diaria.

Principios:

- Jerarquia visual fuerte entre navegacion, contenido y acciones.
- Densidad informativa controlada, apta para lectura prolongada.
- Contraste suficiente sin usar fondos agresivos.
- Superficies claras para contenido y superficies oscuras para navegacion estructural.
- Acentos rojos reservados para acciones primarias, estados relevantes y puntos de foco.

## Patron de layout

### Barra lateral

- Fija en escritorio.
- Fondo azul marino profundo.
- Logo o firma visual en la parte superior.
- Secciones separadas por contexto: operacion, administracion, analitica.
- Item activo con fondo aclarado y contraste evidente.
- Iconos Lucide React alineados a la izquierda del texto.

### Encabezado superior

- Superficie clara.
- Breadcrumbs o ruta actual.
- Acciones globales: notificaciones, sesion, perfil, accesos rapidos.
- Informacion del usuario alineada a la derecha.

### Contenido principal

- Fondo gris azulado muy claro, no blanco puro.
- Contenedor amplio con margenes consistentes.
- Titulo de vista, subtitulo y acciones principales visibles al inicio.
- Tarjetas, tablas y formularios como superficies secundarias dentro del area de trabajo.

## Paleta recomendada

La referencia visual sugiere una combinacion sobria y funcional.

Colores base:

- `--color-fondo-app`: azul grisaceo muy claro.
- `--color-superficie`: blanco suave.
- `--color-lateral`: azul marino profundo.
- `--color-lateral-hover`: azul pizarra.
- `--color-texto-principal`: azul carbon o grafito.
- `--color-texto-secundario`: gris azulado.
- `--color-acento`: rojo administrativo.
- `--color-acento-oscuro`: vino o rojo profundo para estados enfaticos.
- `--color-borde`: gris frio tenue.

Estados:

- Exito: verde controlado, no saturado.
- Alerta: ambar suave.
- Error: rojo alineado con el acento principal.
- Informacion: azul medio neutral.

## Tipografia

La interfaz debe evitar tipografias genericas de sistema como primera opcion.

Propuesta:

- Tipografia principal: `Plus Jakarta Sans`.
- Tipografia secundaria para datos densos o identificadores: `IBM Plex Sans`.

Reglas:

- Titulos con peso semibold o bold.
- Subtitulos y descripcion con peso regular.
- Datos tabulares con tamano legible y espaciado comodo.
- Tamano base de lectura cercano a un documento administrativo bien compuesto.

## Componentes base

### Tarjetas

- Radio moderado, no exagerado.
- Sombra suave y borde sutil.
- Espaciado interior generoso.
- Usarse para resumenes, detalle puntual, boletos, tarjetas documentales y paneles de accion.

### Tabs

- Deben parecer control de vista, no botones sueltos.
- Indicador activo con acento rojo.
- Texto sobrio, con foco en lectura rapida.

### Botones

- Primario: acento rojo.
- Secundario: azul marino o blanco con borde.
- Terciario: texto con icono.
- Los iconos deben venir de Lucide React.

### Tablas

- Encabezados con fondo apenas contrastado.
- Filas compactas pero legibles.
- Filtros visibles encima o dentro del bloque superior.
- Acciones de fila consistentes y alineadas.

### Formularios

- Etiquetas claras en espanol.
- Campos agrupados por bloques: identificacion, documentacion, operacion, mantenimiento.
- Ayuda contextual corta cuando el dato sea ambiguo, por ejemplo `T/C`, `vigencia` o `grupo documental`.

### Tarjetas especiales

- La segunda referencia muestra un patron valido para vistas detalladas con una tarjeta central protagonista.
- Este patron debe reutilizarse para fichas de unidad, documento principal, comprobante, vista previa de QR o resumen operativo puntual.

## Aplicacion por modulo

### Tablero

- Debe combinar KPIs, alertas y listas priorizadas.
- No usar lienzos vacios sin apoyo visual.
- La vista inicial debe mostrar de inmediato el estado operativo del sistema.

### Unidades

- Listado principal con filtros y densidad utilitaria.
- Detalle con tarjeta resumen superior y secciones por bloques.
- Formularios con progresion clara y validacion visible.

### Documentos

- Estados documentales muy visibles.
- Vigencias y vencimientos destacados por color y etiqueta.
- Historial en formato cronologico o tabla compacta.

### Mantenimientos

- Prioridad visual para 3 dias o menos.
- Estado de cada unidad con chips o etiquetas consistentes.
- Secciones claras para programado, en proceso y finalizado.

### Usuarios y roles

- Vista sobria y clara.
- Enfoque en permisos, alcance y trazabilidad.
- Evitar decoracion innecesaria.

## Anti-patrones a evitar

- Fondos completamente planos sin jerarquia.
- Tarjetas gigantescas para informacion pequena.
- Exceso de color o contrastes cansados.
- Tipografia pequena o demasiado ligera.
- Pantallas vacias sin contexto, accion o estado ilustrado.
- Barras laterales sobrecargadas sin agrupacion.
- Formularios largos sin secciones.

## Criterios de aceptacion visual

- La interfaz recuerda la estructura y tono de las referencias, sin copiarlas literalmente.
- Existe una barra lateral oscura con navegacion clara y un area principal clara.
- Los acentos rojos estan dosificados y usados con intencion.
- La lectura prolongada es comoda en tablas, formularios y paneles.
- Los estados vacios, alertas y errores tienen presentacion visual clara.
- El sistema se percibe administrativo, moderno y funcional.

## Pendientes visuales

- Confirmar si la marca final de la aplicacion sera SMT o una submarca operativa.
- Confirmar si se requiere modo compacto para usuarios de escritorio con alta densidad de datos.
- Confirmar si habra soporte movil completo o solo responsive basico para consulta.
- Confirmar si la tarjeta tipo boleto o comprobante debe formar parte del sistema de unidades o solo sirve como referencia de estilo.
