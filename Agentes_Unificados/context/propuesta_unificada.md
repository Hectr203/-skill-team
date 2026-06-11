# Propuesta Unificada de Gobernanza, Arquitectura y Orquestación para la Agencia de Agentes SMT

Este documento establece el marco arquitectónico, las directrices de desarrollo, las reglas de orquestación y el sistema de memoria persistente que regirán a todos los agentes de software y especialistas en el repositorio de **Soluciones de Movilidad Terrestre (SMT)**.

---

## 1. Modelo de Funcionamiento y Comunicación de la Agencia

La agencia de agentes funciona bajo un **esquema híbrido de orquestación**. Para evitar redundancias, costos excesivos en tokens y pérdida de contexto, se prohíbe que los agentes especialistas se auto-invoquen entre sí de forma directa.

### 1.1 Estructura de Comunicación y Flujo
1. **Asistente Principal (Orquestador Maestro):** Es el único punto de entrada de la sesión y el canal de comunicación directo con el humano. Administra el estado global, el ciclo de vida del proyecto y coordina a los subagentes.
2. **Especialistas Atómicos:** Son agentes expertos en un área específica. Reciben tareas delimitadas del Orquestador Maestro, ejecutan su trabajo dentro de su contexto aislado y devuelven un informe técnico estructurado al Orquestador.
3. **Flujo de Trabajo:**
   ```mermaid
   sequenceDiagram
       actor Humano
       participant OP as Orquestador Principal
       participant AR as Analista de Requerimientos
       participant AD as Agente de Desarrollo
       participant AE as Test Engineer / Code Reviewer
       
       Humano->>OP: Plantea Requerimiento / Tarea
       OP->>OP: Inicializa sesión (Verifica y recupera Memoria)
       OP->>AR: Asigna análisis inicial (enviar datos crudos)
       AR-->>OP: Devuelve especificación formal en español (requerimiento.md)
       OP->>Humano: Solicita aprobación de requerimiento
       Humano-->>OP: Aprueba requerimiento
       OP->>AD: Asigna construcción (envía especificación aprobada)
       AD-->>OP: Completa código e informa cambios
       OP->>AE: Asigna pruebas y revisión (envía código y diff)
       AE-->>OP: Reporta conformidad o solicita correcciones
       OP->>Humano: Entrega demo/código validado para aprobación final
       OP->>OP: Cierre sesión (Guarda Memoria Persistente)
   ```

### 1.2 Reglas para Evitar Conflictos entre Agentes
* **Principio de Mínimo Contexto:** Cada subagente especialista recibe únicamente el contexto técnico indispensable para cumplir su tarea actual.
* **Prohibición de Redundancia:** No se crearán agentes con propósitos duplicados. Si un requerimiento puede ser resuelto por el `agente-desarrollo` con la skill `ui-ux-pro-max`, no se debe crear un agente exclusivo de diseño visual.
* **Control de Modificaciones de Código:** Solo el `agente-desarrollo` and el `agente-base-datos` están autorizados para modificar el código fuente y el esquema de base de datos. Los agentes de pruebas (`test-engineer`), calidad (`code-reviewer`) y seguridad (`security-auditor`) operan de forma estrictamente analítica y de verificación.

---

## 2. Roles, Responsabilidades y Skills Integradas

### 2.1 Matriz de Agentes y Responsabilidades

| Agente Especialista | Responsabilidad Principal | Entregable Clave |
| :--- | :--- | :--- |
| **Analista de Requerimientos** | Recopilar información del humano, estructurar casos de uso, reglas de negocio y criterios de aceptación. | `requerimiento.md` en su subcarpeta correspondiente. |
| **Agente de Desarrollo** | Construir el software respetando la Clean Architecture (backend) y Atomic Design (frontend). | Código fuente compilable y libre de errores en TypeScript. |
| **Agente de Base de Datos** | Diseñar, validar y optimizar la persistencia relacional con PostgreSQL. | `schema.prisma`, migraciones numeradas y scripts de semillas (`seed.ts`). |
| **Agente de Testeo (Test Engineer)** | Diseñar estrategias de pruebas unitarias, integración y E2E. Aplicar el patrón *Prove-It* ante bugs. | Reporte de cobertura y suite de pruebas automatizadas aprobadas. |
| **Agente de Diseño (UI/UX)** | Asegurar consistencia visual responsiva, paleta de colores y componentes atómicos en Tailwind. | `MASTER.md` del sistema de diseño y componentes atómicos base. |
| **Agente de Documentación** | Registrar cambios del sistema, mantener bitácoras y documentar decisiones técnicas relevantes. | Registros de Arquitectura (ADR) y bitácoras de sesión actualizadas. |

### 2.2 Integración de las Skills Existentes
Todos los agentes deben invocar obligatoriamente las siguientes skills unificadas en el directorio `Agentes_Unificados/skills/`:
* **`backend-dominio-limpio`:** Obligatoria para cualquier cambio de lógica de negocio o servicios de API en Node.js/Express.
* **`prisma-base-de-datos`:** Obligatoria para toda persistencia relacional con PostgreSQL, asegurando la no utilización de consultas SQL crudas.
* **`ui-ux-pro-max`:** Ubicada en `skills/ui-ux-pro-max/`. Es el manual maestro de diseño, tipografía, paletas de colores y accesibilidad, alineado con el Atomic Design.
* **`commits-espanol`:** Aplica en todo el flujo de trabajo de Git, forzando los mensajes de commits y la documentación en español formal.
* **`ahorro-contexto`:** Utilizada en cada sesión para limitar la lectura de archivos pesados (`node_modules`, `dist`, `.git`) y optimizar el uso de tokens.

---

## 3. Arquitectura del Backend y Base de Datos

El backend se regirá de forma estricta por la **Clean Architecture** (Arquitectura Limpia) y el diseño hexagonal, asegurando el bajo acoplamiento con librerías externas y motores de bases de datos.

### 3.1 Estructura del Código Backend
Todo desarrollo se aloja en carpetas modulares cohesivas dentro de `src/modules/<nombre-modulo>/`:

```txt
src/modules/viajes/
├── viajes.routes.ts         # Rutas, middlewares de Express y validadores
├── viajes.controller.ts     # Controlador: maneja Req/Res y conversión a DTOs
├── viajes.service.ts        # Caso de Uso / Lógica de negocio (Dominio Limpio)
└── viajes.repository.ts     # Repositorio de Persistencia (Infraestructura Prisma)
```

* **Controladores:** Tienen prohibido importar o invocar la instancia de PrismaClient. Su única responsabilidad es recibir peticiones HTTP, parsear parámetros, validar DTOs, invocar al Servicio correspondiente y responder códigos HTTP estándar en español.
* **Servicios (Casos de Uso):** Contienen la lógica de negocio pura (ej. "validar que el chofer base asignado esté disponible y no exceda sus horas de jornada"). Dependen únicamente de interfaces de repositorios para mantener el desacoplamiento.
* **Repositorios:** Implementan el acceso a datos. Es la única capa que interactúa directamente con Prisma.

### 3.2 Reglas para Base de Datos y ORM (Prisma + PostgreSQL)
* **Motor Definitivo:** PostgreSQL. Se prohíbe el uso de SQL Server debido a su inviabilidad de costes en la nube para el proyecto.
* **Uso Exclusivo de Prisma:** Queda prohibido el uso de consultas SQL crudas (`$queryRaw`), salvo justificación de optimización extrema autorizada por el Arquitecto Principal.
* **Modelado en `schema.prisma`:**
  * **Tablas (Modelos):** Escritos en `PascalCase` singular en español (ej. `model Unidad`, `model Operador`).
  * **Columnas (Campos):** Escritos en `camelCase` en español (ej. `placaVehículo`, `capacidadPasajeros`).
  * **Identificadores:** IDs de tipo CUID obligatorio (`id String @id @default(cuid())`).
  * **Soft Delete (Borrado Lógico Obligatorio):** Ningún registro se elimina físicamente de la base de datos. Se debe incluir el campo `eliminadoEn DateTime?`. Todos los repositorios deben filtrar de forma transparente `where: { eliminadoEn: null }`.
  * **Semillas (Seeds):** Ubicadas en `prisma/seed.ts`, deben poblar automáticamente la base de datos con los datos maestros iniciales (ej. tipos de unidades Mercedes-Benz, Volvo, Sprinter y roles iniciales del sistema).

---

## 4. Arquitectura del Frontend

El frontend debe seguir una **arquitectura modular por componentes altamente reutilizables** basada en el modelo **Atomic Design**.

### 4.1 Organización de Archivos en el Frontend
```txt
frontend/src/
├── components/                  # Componentes reutilizables globales
│   ├── atomos/                  # Botón, Input, Etiqueta, Icono SVG (sin dependencias)
│   ├── moleculas/               # Campo de formulario (Input + Etiqueta), Buscador
│   ├── organismos/              # Tabla de unidades, Formulario de registro, Sidebar
│   └── templates/               # AppShell (estructura responsiva sin datos)
├── modules/                     # Módulos funcionales autocontenidos
│   └── logistica/
│       └── asignacion-ruta/
│           ├── components/      # Componentes exclusivos de este módulo
│           ├── services/        # Llamadas Axios específicas
│           ├── types/           # Interfaces de TypeScript locales
│           └── index.tsx        # Vista u orquestador visual del submódulo
├── hooks/                       # Custom hooks globales
├── pages/                       # Vistas de páginas de alto nivel (Rutas)
├── services/                    # Clientes y configuraciones base de Axios
├── stores/                      # Estados globales ligeros con Zustand
└── types/                       # Tipos globales de TypeScript
```

### 4.2 Reglas de Desarrollo Frontend
* **Componentes Base Primero:** Antes de construir la UI de un módulo, se deben definir o reutilizar los átomos y moléculas ubicados en `components/`. Esto garantiza que los cambios visuales o de estilos (ej. cambiar el color de los botones primarios) se realicen en un solo punto central.
* **Aislamiento de API:** Los componentes de React tienen prohibido realizar llamadas HTTP directas usando `fetch` o `axios` en línea. Deben importar funciones tipadas desde los archivos de la carpeta `services/`.
* **Herramientas Visuales Obligatorias:**
  * **Lucide React:** Único set de iconos permitido. Se prohíbe terminantemente el uso de emojis como iconos de interfaz.
  * **Sonner:** Utilizado para todas las notificaciones toast y avisos en pantalla.
  * **Tailwind CSS:** Para todos los estilos y diseño responsivo, siguiendo las directrices de `ui-ux-pro-max`.

---

## 5. Metodología de Desarrollo Flexible

El marco de trabajo por defecto es **Scrum**, ya que permite una entrega incremental estructurada, pero el sistema está diseñado para alternar dinámicamente hacia otras metodologías de acuerdo a la escala y velocidad del requerimiento.

### 5.1 Proceso Scrum (Predeterminado)
1. **Levantamiento:** El analista genera los requerimientos en `requerimiento.md` y redacta las Historias de Usuario con criterios de aceptación claros.
2. **Priorización:** Se ordenan los entregables en el Backlog del proyecto.
3. **Desarrollo Guiado por Especificaciones:** El programador y el ingeniero de pruebas trabajan en paralelo utilizando el mismo documento `requerimiento.md` para evitar desviaciones.
4. **Validación:** El Test Engineer ejecuta las pruebas de aceptación. Si fallan, reporta mediante el patrón *Prove-It* al programador.
5. **Cierre:** Se requiere la validación del humano para el despliegue del incremento de software.

### 5.2 Flexibilidad de Marcos de Trabajo
El Orquestador Maestro puede cambiar el marco activo a petición del humano o del desarrollador:
* **Kanban:** Optimiza tareas de mantenimiento continuo de bugs o UI rápidas. Se elimina el concepto de Sprints rígidos y se enfoca en limitar el *Work In Progress (WIP)* y el flujo continuo en un tablero local.
* **Cascada / Modelo en V:** Adecuado para migraciones estructurales masivas de base de datos o APIs críticas de terceros. Fuerza una fase de diseño técnico y auditoría de seguridad exhaustiva antes de escribir cualquier línea de código.
* **Desarrollo Incremental/Iterativo:** Enfocado a prototipos rápidos y validación visual constante con el humano.

> [!IMPORTANT]
> **Independencia del Marco de Trabajo:** El cambio de metodología metodológica (Scrum, Kanban, Cascada) **NUNCA** modifica ni reduce los estándares técnicos. Clean Architecture, Clean Code, el Atomic Design y el uso obligatorio de Prisma con PostgreSQL se aplican en el 100% de los escenarios.

---

## 6. El Humano en el Ciclo (Human-in-the-Loop)

Para evitar desviaciones de la lógica de negocio real de SMT, la validación del humano es una **puerta de calidad obligatoria** en las siguientes fases críticas del ciclo:

1. **Aprobación de Requerimientos:** El analista de requerimientos debe obtener la aprobación explícita del humano sobre las historias de usuario y el alcance antes de pasárselo al agente de desarrollo.
2. **Decisiones de Arquitectura Excepcionales:** Cualquier cambio que altere el esquema de la base de datos, agregue dependencias NPM críticas o requiera el uso de consultas SQL crudas debe ser aprobado por el humano.
3. **Cierre de Entregables e Incrementos:** El paso a producción o la marcación de una tarea de desarrollo como completada requiere que el humano valide el walkthrough técnico y las pruebas de interfaz en un ambiente local o de staging.

---

## 7. Control de Idioma y Coherencia Lingüística

El proyecto está catalogado como **estrictamente en español**. Esto maximiza la legibilidad para el equipo de desarrollo, soporte y auditores locales.

* **Obligatorio en Español:**
  * Comentarios de código, logs y mensajes de error del sistema.
  * Documentación técnica, requerimientos, historias de usuario, casos de prueba y ADRs.
  * Nombres de tablas, vistas, campos, relaciones y datos de semillas en la base de datos (ej. `model Viaje`, `placaVehículo`).
  * Variables, funciones, clases, controladores, servicios y DTOs en el código (ej. `const calcularConsumoCombustible = () => {}`, `ViajesController`).
* **Permitido en Inglés:**
  * Palabras reservadas del lenguaje (ej. `const`, `class`, `async`, `await`).
  * Convenciones de frameworks y dependencias estándar (ej. `routes`, `controller`, `service`, `repository`, `cuid()`, `schema.prisma`).
  * Cabeceras HTTP, métodos REST estándar (`GET`, `POST`, `PATCH`, `DELETE`) y keywords de dependencias.

---

## 8. Integración de Memoria Persistente y Seguridad

Para evitar la pérdida de contexto entre sesiones con IA, se establece un flujo automatizado de memoria local y en la nube, dividiendo estrictamente los datos según su sensibilidad.

### 8.1 Criterios de Selección de Herramienta de Memoria
* **Cloud Mem:** Diseñado para la nube. Se utiliza exclusivamente para elementos de frontend, ajustes visuales rápidos, componentes React, flujos CSS y experiencia de usuario ágil.
* **Mem Palace:** Diseñado de forma local y cifrado. Se utiliza obligatoriamente para la lógica de backend, estructuras de base de datos PostgreSQL, reglas de inventario de SMT, consumo de combustible, secretos del sistema, logs y decisiones técnicas estratégicas.

> [!CAUTION]
> **Prohibición de Datos Críticos en la Nube:** Queda estrictamente prohibido guardar credenciales, llaves de API, lógica de persistencia sensible o reglas operativas de producción de SMT en Cloud Mem. Todo ese contexto debe mantenerse cifrado en local mediante Mem Palace.

### 8.2 Scripts Locales de Soporte en Python
Ubicados en la carpeta `skills/ahorro-contexto/scripts/`:

#### A. Script de Validación y Arranque (`arranque.py`)
Antes de iniciar cualquier tarea crítica en una sesión, el asistente principal debe ejecutar este script. El script verifica si el entorno cuenta con las dependencias necesarias de cifrado (`cryptography` o `pycryptodome`) y realiza la recuperación del contexto indexado mediante un **prompt de arranque compacto de máximo 170 palabras**.

```python
# skills/ahorro-contexto/scripts/arranque.py
import os
import sys

def verificar_instalacion():
    print("[-] Verificando dependencias de memoria persistente...")
    try:
        import cryptography
        print("[+] Cryptography instalado correctamente.")
    except ImportError:
        print("[!] ADVERTENCIA: 'cryptography' no está instalado. Instalando...")
        # Lógica de instalación local automática
    
    # Comprobar existencia de archivos locales de Mem Palace cifrados
    if os.path.exists(".memoria_palacio_cifrada"):
        print("[+] Archivo de Mem Palace detectado. Listo para descifrar contexto.")
    else:
        print("[!] No se detectó Mem Palace previo. Creando nuevo espacio local seguro.")

if __name__ == "__main__":
    verificar_instalacion()
```

#### B. Script de Persistencia en Mem Palace (`mem_palace.py`)
Script local en Python encargado de cifrar la información de la sesión crítica utilizando una clave simétrica local (almacenada en un archivo excluido por `.gitignore`) y guardarla en el archivo `.memoria_palacio_cifrada`.

```python
# skills/ahorro-contexto/scripts/mem_palace.py
import os
from cryptography.fernet import Fernet

def guardar_contexto_critico(datos_contexto: str):
    # Genera o lee clave local fuera de control de versiones
    ruta_clave = ".mem_palace_key"
    if not os.path.exists(ruta_clave):
        clave = Fernet.generate_key()
        with open(ruta_clave, "wb") as f:
            f.write(clave)
    else:
        with open(ruta_clave, "rb") as f:
            clave = f.read()
            
    fernet = Fernet(clave)
    datos_cifrados = fernet.encrypt(datos_contexto.encode())
    
    with open(".memoria_palacio_cifrada", "wb") as f:
        f.write(datos_cifrados)
    print("[+] Contexto crítico cifrado exitosamente en Mem Palace local.")
```

#### C. Script de Cierre de Sesión y Reporte (`cierre.py`)
Al finalizar el trabajo, este script recopila los cambios de desarrollo, tareas pendientes, decisiones técnicas tomadas y compila el informe final, actualizando de forma automática tanto **Cloud Mem** (datos visuales de frontend) como **Mem Palace** (cifrando la lógica del backend y BD).

---

## 9. Lista de Verificación y Go-Live de la Sesión

Antes de que un agente de la agencia de desarrollo dé por completado su trabajo en una sesión, el Orquestador Principal debe obligatoriamente verificar la siguiente lista:

- [ ] **Idioma:** Todo el código escrito, comentarios y logs están estrictamente en español.
- [ ] **Backend:** Se respeta la separación Controladores -> Servicios -> Repositorios. Ningún controlador importa a Prisma.
- [ ] **Base de Datos:** Los deletes lógicos están implementados y no hay sentencias SQL crudas en los repositorios.
- [ ] **Frontend:** Los componentes creados se clasificaron correctamente según Atomic Design en `components/` y las APIs se invocan a través de servicios tipados.
- [ ] **Memoria Cierre:** Se han ejecutado los scripts de cierre actualizando tanto Cloud Mem como cifrando la lógica de negocio sensible mediante Mem Palace.
