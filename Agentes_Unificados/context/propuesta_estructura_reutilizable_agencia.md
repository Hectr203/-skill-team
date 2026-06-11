# Propuesta de Estructura Reutilizable para la Agencia

## Objetivo

Separar de forma explicita los **agentes y skills reutilizables** de los **agentes y skills especificos de un proyecto**, para que la agencia pueda reutilizarse en cualquier IA, cualquier proyecto y cualquier rubro sin arrastrar contexto de dominio que no corresponda.

La referencia de dominio usada para esta propuesta es el conjunto de skills SMT como:

- `base_reutilizable/skills/verticales/transporte/operacion/conductor-transporte-personal`
- `base_reutilizable/skills/verticales/transporte/operacion/administrador-equipos-moviles-transporte`
- `base_reutilizable/skills/verticales/transporte/dominio/experto-logistica-transporte-personal`

Estas skills son utiles como ejemplo de habilidades de dominio, pero no deben vivir en la misma capa que las skills generales de arquitectura, frontend, backend o memoria.

---

## Diagnostico de la estructura actual

Hoy `Agentes_Unificados/skills/` mezcla dos categorias distintas:

1. **Skills base de la agencia**
   Ejemplos:
   - `backend-dominio-limpio`
   - `prisma-base-de-datos`
   - `ui-ux-pro-max`
   - `ahorro-contexto`
   - `commits-espanol`
   - `creador-de-habilidades`

2. **Skills de dominio SMT**
   Ejemplos:
   - `conductor-transporte-personal`
   - `administrador-equipos-moviles-transporte`
   - `experto-logistica-transporte-personal`

El problema de esta mezcla es que la agencia parece universal, pero su carpeta principal de skills ya viene contaminada por un dominio concreto. Eso dificulta reutilizarla en salud, retail, fintech, manufactura o cualquier otro proyecto.

---

## Principio rector

La agencia debe organizarse en dos capas:

1. **Base reutilizable de la agencia**
   Contiene agentes, skills, contexto y plantillas que pueden usarse en cualquier proyecto.

2. **Capa de proyecto**
   Contiene agentes, skills, contexto y reglas que solo aplican a un proyecto concreto.

La base no depende del proyecto.
El proyecto si depende de la base.

Dentro de la base reutilizable puede existir una subcapa de **verticales reutilizables** para skills que no son universales, pero si reutilizables en varios proyectos del mismo sector.

---

## Estructura propuesta

```txt
Agentes_Unificados/
├── base_reutilizable/
│   ├── agentes/
│   ├── skills/
│   │   ├── arquitectura/
│   │   ├── backend/
│   │   ├── frontend/
│   │   ├── datos/
│   │   ├── calidad/
│   │   ├── seguridad/
│   │   ├── memoria/
│   │   ├── utilidades/
│   │   └── verticales/
│   │       └── transporte/
│   │           ├── dominio/
│   │           └── operacion/
│   ├── context/
│   └── plantillas/
├── proyectos/
│   └── smt/
│       ├── agentes/
│       ├── skills/
│       │   ├── dominio/
│       │   ├── operacion/
│       │   └── integraciones/
│       ├── context/
│       └── plantillas/
├── agentes/
├── skills/
└── context/
```

---

## Funcion de cada carpeta

### `base_reutilizable/`

Es el nucleo comun de la agencia. Debe contener solo elementos que funcionen en cualquier rubro.

#### `base_reutilizable/agentes/`

Aqui viven los agentes base, por ejemplo:

- `agente-orquestador.md`
- `agente-backend.md`
- `agente-frontend.md`
- `agente-base-de-datos.md`
- `revisor-de-codigo.md`
- `auditor-de-seguridad.md`
- `ingeniero-de-pruebas.md`

Estos agentes no deben mencionar SMT ni transporte. Deben describir responsabilidades generales.

#### `base_reutilizable/skills/`

Se agrupan por tipo:

- `arquitectura/`
  Skills como Clean Architecture, arquitectura hexagonal, modularidad, documentacion tecnica.

- `backend/`
  Skills como `backend-dominio-limpio`.

- `frontend/`
  Skills como `ui-ux-pro-max`, `frontend-design`.

- `datos/`
  Skills como `prisma-base-de-datos`.

- `calidad/`
  Skills de revision, testing, validacion y criterios de salida.

- `seguridad/`
  Skills de hardening, secretos, control de accesos, auditoria.

- `memoria/`
  Skills como `ahorro-contexto`, arranque/cierre de sesion, politica de memoria persistente.

- `utilidades/`
  Skills auxiliares como `commits-espanol`, `creador-de-habilidades` y herramientas de soporte.

- `verticales/`
  Skills reutilizables por rubro. Aqui viven habilidades que no son universales, pero tampoco dependen de un solo proyecto.
  Ejemplo: transporte, salud, retail, manufactura.

#### `base_reutilizable/context/`

Documentos generales de la agencia:

- principios globales
- reglas de orquestacion
- convenciones de idioma
- criterios para seleccionar skills
- metodologia por defecto

#### `base_reutilizable/plantillas/`

Plantillas reutilizables:

- plantilla de skill
- plantilla de agente
- plantilla de contexto de proyecto
- plantilla de manifiesto de proyecto

---

### `proyectos/smt/`

Contiene solo lo que depende de SMT como proyecto concreto.

#### `proyectos/smt/agentes/`

Agentes adaptados al proyecto SMT, por ejemplo:

- `asistente-principal-smt.md`
- `agente-orquestador-smt.md`

Estos agentes pueden extender los agentes base con reglas del negocio SMT.

#### `proyectos/smt/skills/`

Separadas por naturaleza:

- `dominio/`
  Reglas de negocio, lenguaje del sector, entidades del problema.

- `operacion/`
  Flujos reales, comportamiento de usuarios, restricciones operativas.

- `integraciones/`
  APIs, sistemas externos, telemetria, GPS, servicios privados, conectores de negocio.

Ubicacion sugerida para skills **exclusivas** de SMT:

```txt
proyectos/smt/skills/dominio/
├── reglas-comerciales-smt/
└── politicas-operativas-smt/

proyectos/smt/skills/operacion/
└── flujos-internos-smt/
```

Ubicacion recomendada para las skills actuales de transporte cuando se quieran reutilizar en otros proyectos del mismo sector:

```txt
base_reutilizable/skills/verticales/transporte/dominio/
└── experto-logistica-transporte-personal/

base_reutilizable/skills/verticales/transporte/operacion/
├── conductor-transporte-personal/
└── administrador-equipos-moviles-transporte/
```

#### `proyectos/smt/context/`

Documentos propios del proyecto:

- contexto del negocio
- arquitectura aplicada a SMT
- stack seleccionado para SMT
- reglas de seguridad del proyecto
- memoria de decisiones del proyecto

#### `proyectos/smt/plantillas/`

Plantillas propias del proyecto cuando haga falta:

- historia de usuario SMT
- ficha de ruta
- especificacion de incidencia
- plantilla de modulo del dominio

---

## Regla de carga de contexto

La agencia debe seguir este orden:

1. Cargar primero la **base reutilizable**.
2. Detectar el proyecto activo.
3. Cargar despues el contexto del proyecto.
4. Importar solo las skills especificas del proyecto cuando la tarea lo requiera.

Esto evita que una skill de transporte contamine una sesion sobre otro rubro.

---

## Regla de identificacion del proyecto activo

Cada proyecto debe tener un manifiesto propio. Ejemplo sugerido:

```txt
Agentes_Unificados/proyectos/smt/context/manifiesto-proyecto.md
```

Contenido minimo recomendado:

- nombre del proyecto
- dominio o rubro
- stack tecnico
- skills de dominio habilitadas
- agentes de proyecto habilitados
- restricciones especiales
- reglas de memoria

Con esto, la agencia puede saber:

- que skills son generales
- que skills son del proyecto actual
- cuando debe cargarlas
- cuando debe ignorarlas

---

## Criterio para decidir si una skill es reutilizable o especifica

Haz esta pregunta:

**Si elimino toda referencia a un proyecto concreto, la skill sigue teniendo sentido?**

Si la respuesta es **si** y sirve en cualquier rubro, la skill va a `base_reutilizable/`.
Si la respuesta es **si**, pero solo reutiliza dentro de un sector, la skill va a `base_reutilizable/skills/verticales/<sector>/`.
Si la respuesta es **no**, la skill va a `proyectos/<proyecto>/skills/`.

Ejemplos:

- `backend-dominio-limpio`: reutilizable
- `prisma-base-de-datos`: reutilizable
- `ui-ux-pro-max`: reutilizable
- `conductor-transporte-personal`: reutilizable por vertical transporte
- `administrador-equipos-moviles-transporte`: reutilizable por vertical transporte
- `experto-logistica-transporte-personal`: reutilizable por vertical transporte

---

## Propuesta de migracion desde la estructura actual

### Skills que deben moverse a la base reutilizable

- `skills/ahorro-contexto`
- `skills/backend-dominio-limpio`
- `skills/commits-espanol`
- `skills/creador-de-habilidades`
- `skills/frontend-design`
- `skills/prisma-base-de-datos`
- `skills/ui-ux-pro-max`

### Skills que deben moverse a base reutilizable por vertical transporte

- `base_reutilizable/skills/verticales/transporte/operacion/conductor-transporte-personal`
- `base_reutilizable/skills/verticales/transporte/operacion/administrador-equipos-moviles-transporte`
- `base_reutilizable/skills/verticales/transporte/dominio/experto-logistica-transporte-personal`

### Skills que deben moverse al proyecto SMT

- skills que describan reglas exclusivas de SMT, politicas internas, clientes, contratos o decisiones que no apliquen a otro operador

### Agentes reutilizables

- `agentes/agente-backend.md`
- `agentes/agente-base-de-datos.md`
- `agentes/agente-frontend.md`
- `agentes/agente-orquestador.md`
- `agentes/revisor-de-codigo.md`
- `agentes/auditor-de-seguridad.md`
- `agentes/ingeniero-de-pruebas.md`

### Agentes que conviene duplicar o especializar por proyecto

- `asistente-principal.md`
- cualquier orquestador que incluya reglas del negocio SMT
- cualquier agente que mencione transporte, rutas, choferes o flota como supuesto central

---

## Estructura minima de archivos recomendada

```txt
base_reutilizable/
├── agentes/
│   ├── agente-orquestador.md
│   ├── agente-backend.md
│   ├── agente-frontend.md
│   └── agente-base-de-datos.md
├── skills/
│   ├── backend/
│   │   └── backend-dominio-limpio/
│   ├── datos/
│   │   └── prisma-base-de-datos/
│   ├── frontend/
│   │   ├── ui-ux-pro-max/
│   │   └── frontend-design/
│   ├── memoria/
│   │   └── ahorro-contexto/
│   ├── verticales/
│   │   └── transporte/
│   │       ├── dominio/
│   │       │   └── experto-logistica-transporte-personal/
│   │       └── operacion/
│   │           ├── conductor-transporte-personal/
│   │           └── administrador-equipos-moviles-transporte/
│   └── utilidades/
│       ├── commits-espanol/
│       └── creador-de-habilidades/
└── context/
    ├── principios-agencia.md
    ├── reglas-orquestacion.md
    └── convenciones-globales.md
```

```txt
proyectos/smt/
├── agentes/
│   └── asistente-principal-smt.md
├── skills/
│   ├── dominio/
│   │   └── experto-logistica-transporte-personal/
│   └── operacion/
│       ├── conductor-transporte-personal/
│       └── administrador-equipos-moviles-transporte/
└── context/
    ├── manifiesto-proyecto.md
    ├── contexto-negocio.md
    └── reglas-smt.md
```

---

## Recomendacion operativa

No conviene mover de golpe la estructura actual sin un paso intermedio. Lo mas sano es:

1. Crear la nueva estructura.
2. Clasificar los agentes y skills actuales.
3. Copiar primero a la nueva ubicacion.
4. Ajustar referencias y manifiestos.
5. Validar que la agencia siga resolviendo bien el contexto SMT.
6. Solo despues retirar o archivar la estructura antigua.

---

## Conclusion

La agencia debe comportarse como un **motor reusable** con una **capa de proyecto acoplable**.

La base reutilizable contiene arquitectura, frontend, backend, datos, seguridad, memoria, utilidades generales y verticales reutilizables.
El proyecto SMT contiene sus agentes, contexto y solo las reglas exclusivas del proyecto.

Con esta separacion se consigue:

- reutilizar la agencia en cualquier IA o rubro
- mantener aislado el contexto de cada proyecto
- importar skills propias sin contaminar la base general
- crear nuevas skills especificas sin romper la reutilizacion
- facilitar que la agencia detecte que pertenece al contexto general y que pertenece al proyecto actual
