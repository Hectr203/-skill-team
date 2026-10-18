# Architecture Quality Gate

Esta lista guía una revisión manual; no demuestra que el validador automático compruebe todos estos criterios. Los ejemplos de lenguaje se adaptan al perfil aprobado. En React Native conservar primitives y navegación nativos.

### Structural integrity
Place generic controls in components/ui and business UI in the appropriate arquitectura modular por dominio módulo; preserve public APIs and explicit public contracts without cycles.
- [ ] Lógica del caso de uso en hooks y servicios de su módulo.
- [ ] No monolithic files. Each component in its own file.
- [ ] Datos de demostración separados de fuentes reales y ubicados en su módulo; no reemplazar contenido real por mocks.

### Type safety and syntax
- [ ] Contratos de props según el lenguaje del perfil: JSDoc en JavaScript o tipos en TypeScript.
- [ ] Archivos sintácticamente válidos en el lenguaje del proyecto.
- [ ] Placeholders from template (e.g., `StitchComponent`) have been replaced with actual names.
- [ ] Navigation screen params are typed with `NativeStackScreenProps` or equivalent.

### React Native primitives
- [ ] No HTML elements (`div`, `span`, `p`, `img`, `button`). Only React Native components.
- [ ] All text wrapped in `Text` components. No raw strings inside `View`.
- [ ] `Pressable` used for interactive elements (not `TouchableOpacity` or `TouchableHighlight`).
- [ ] `FlatList` used for dynamic/long lists (not `ScrollView` with `.map()`).
- [ ] `Image` components have explicit `width` and `height` or `aspectRatio`.

### Styling
- [ ] All styles defined via `StyleSheet.create()` at the bottom of the file.
- [ ] No inline style objects (use `StyleSheet` references).
- [ ] No hardcoded hex values. Colors referenced from the project’s shared design tokens.
- [ ] Shadows use `Platform.select()` for iOS/Android differences.
- [ ] `flexDirection` explicitly set where row layout is needed (default is `column`).

### Accessibility
- [ ] Interactive elements have `accessibilityLabel` and `accessibilityRole`.
- [ ] Images have descriptive `accessibilityLabel`.
- [ ] Toggle/checkbox elements use `accessibilityState`.

### Platform handling
- [ ] Top-level screens wrapped with `SafeAreaView` from `react-native-safe-area-context`.
- [ ] Platform-specific code uses `Platform.select()` or `Platform.OS` checks.
- [ ] Responsive dimensions use `useWindowDimensions()` (not hardcoded pixel values for screen-relative sizing).
