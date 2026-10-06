# Gestión de Contextos de Clientes — Agencia Principal

Este directorio almacena el contexto comercial, requisitos de negocio y acuerdos específicos de cada cliente atendido por la **Agencia Principal**.

---

## 1. Regla de Aislamiento Estricto
Cada cliente cuenta con un subdirectorio exclusivo bajo `contexts/clients/<nombre_cliente>/`.
> [!IMPORTANT]
> **Privacidad y No Fuga de Datos:** Queda terminantemente prohibido cruzar, importar o referenciar información confidencial, claves o bases de datos de un cliente hacia proyectos de otro cliente salvo autorización explícita por escrito del operador humano.

---

## 2. Estructura Recomendada por Cliente

```txt
contexts/clients/<nombre_cliente>/
├── perfil.md                  # Razón social, contactos clave, sector y canales oficiales
├── acuerdos.md                # Tarifas pactadas, plazos, hitos y contratos
└── requerimientos_generales.md# Políticas internas y restricciones de seguridad del cliente
```

---

## 3. Plantilla Base para `perfil.md`

```markdown
# Perfil del Cliente: [Nombre de la Empresa o Cliente]

- **ID del Cliente:** [slug-cliente]
- **Persona de Contacto:** [Nombre y puesto]
- **Canal de Comunicación Primario:** [WhatsApp / Correo / Slack]
- **Sector de Industria:** [Ejemplo: Transporte / Logística / Salud / Finanzas]
- **Marcas Asociadas:** [Vincular a contexts/brands/<marca>]
- **Proyectos Activos:** [Vincular a contexts/projects/<proyecto>]
```
