---
name: redux
description: Guía de gestión de estado global y predecible en React con Redux Toolkit y Zustand. Usar cuando el estado compartido entre múltiples módulos o dominios de negocio justifique un store centralizado, aplicando la filosofía Ponytail para evitar sobreingeniería.
---

# Gestión de Estado con Redux Toolkit y Zustand

Esta skill proporciona las directivas, patrones y mejores prácticas para la gestión de estado global en aplicaciones React dentro de la arquitectura de **Monorepo dividido** y **Atomic Design Compositivo** de la Agencia de Proyectos.

## Principio Ponytail de Gestión de Estado

Antes de introducir un store global como Redux, aplicar la escalera de decisión:
1. **¿Es estado de un solo componente?** -> `useState` nativo de React.
2. **¿Es estado compartido entre padre e hijos inmediatos?** -> Levantar el estado (*lifting state up*) mediante props.
3. **¿Es estado de servidor (datos de API, caché, invalidación)?** -> React Query / TanStack Query o SWR (evita duplicar respuestas de API en el store de cliente).
4. **¿Es estado de UI global ligero (tema, sidebar colapsado)?** -> React Context o Zustand store simple.
5. **¿Es estado de negocio complejo, transaccional, con múltiples mutaciones o flujos derivados?** -> **Redux Toolkit (RTK)** o **Zustand**.

---

## Patrón de Integración con la Arquitectura Frontend

En la arquitectura modular por dominio de la agencia (`frontend/src/`):

1. **Estado Global Transversal (`shared/store/`)**:
   - Sesión de usuario, tokens de autenticación, permisos RBAC activos.
   - Configuración global de entorno y preferencias del sistema.
   - Instancia raíz del store (`rootStore.ts`).

2. **Slices o Stores de Dominio (`modules/<modulo>/store/`)**:
   - Cada dominio de negocio complejo (ej. `carrito`, `ventas`, `facturacion`) puede encapsular su propio slice (`<submodulo>Slice.ts`).
   - Los reducers y acciones son privados al módulo salvo los selectores expuestos en el `index.ts` público del módulo.

---

## Estructura Recomendada con Redux Toolkit (RTK)

```typescript
// modules/ventas/store/ventasSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface VentasState {
  itemsSeleccionados: Array<{ id: string; cantidad: number; precio: number }>;
  descuentoGlobal: number;
  estadoCaja: 'abierta' | 'cerrada';
}

const initialState: VentasState = {
  itemsSeleccionados: [],
  descuentoGlobal: 0,
  estadoCaja: 'abierta',
};

export const ventasSlice = createSlice({
  name: 'ventas',
  initialState,
  reducers: {
    agregarItem: (state, action: PayloadAction<{ id: string; cantidad: number; precio: number }>) => {
      const existente = state.itemsSeleccionados.find(i => i.id === action.payload.id);
      if (existente) {
        existente.cantidad += action.payload.cantidad;
      } else {
        state.itemsSeleccionados.push(action.payload);
      }
    },
    limpiarVenta: (state) => {
      state.itemsSeleccionados = [];
      state.descuentoGlobal = 0;
    },
  },
});

export const { agregarItem, limpiarVenta } = ventasSlice.actions;
export default ventasSlice.reducer;
```

---

## Alternativa Ligera con Zustand

Para flujos donde se busca máxima ligereza sin boilerplate de acciones ni reducers:

```typescript
// shared/store/useAuthStore.ts
import { create } from 'zustand';

interface AuthState {
  usuario: { id: string; email: string; rol: string } | null;
  token: string | null;
  setAuth: (usuario: { id: string; email: string; rol: string }, token: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  usuario: null,
  token: null,
  setAuth: (usuario, token) => set({ usuario, token }),
  logout: () => set({ usuario: null, token: null }),
}));
```

---

## Reglas Innegociables

1. **Nunca duplicar datos de servidor en el store**: Los endpoints de datos deben consumirse con hooks tipados (`useQuery` o hooks locales de servicio); Redux se reserva para estado transaccional del cliente.
2. **Selectores memorizados**: Usar `createSelector` de Reselect en selectores computados para evitar renders innecesarios.
3. **Inmutabilidad estricta**: RTK utiliza Immer internamente; en stores planos o Zustand, respetar siempre la inmutabilidad de estados.
4. **Cero persistencia de secretos**: Tokens de sesión solo en memoria o cookies HttpOnly seguras; jamás almacenar contraseñas ni datos sensibles sin cifrar en localStorage o redux-persist.
