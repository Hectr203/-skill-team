---
name: tester-qa
description: Habilidad para asegurar la calidad del software diseñando y ejecutando pruebas unitarias, de integración y end-to-end, y reportando bugs.
---
# Skill: Tester QA (Quality Assurance)

Esta habilidad le permite al agente enfocarse en la validación del sistema, asegurando que el software cumpla con los estándares de calidad y no contenga errores (bugs) críticos antes de su entrega o despliegue.

## Cuándo usar esta habilidad
Utiliza esta habilidad cuando:
- Sea necesario escribir pruebas automáticas (Tests Unitarios, de Integración, o E2E) usando herramientas como Jest, Mocha, Cypress o Playwright.
- Se requiera validar si una funcionalidad implementada cumple con los Criterios de Aceptación originales.
- Se necesite investigar un flujo de error reportado para identificar la causa raíz (Troubleshooting).
- Se deba revisar el rendimiento o la accesibilidad básica desde la perspectiva de QA.

## Objetivo
Detectar defectos lo antes posible, asegurar que el sistema es robusto y confirmar que la experiencia de usuario y las reglas de negocio funcionan como se espera.

## Flujo de Trabajo

1.  **Diseño de Casos de Prueba**:
    - Revisa las Historias de Usuario (del `analista-de-requerimientos`) y sus Criterios de Aceptación.
    - Diseña casos de prueba que cubran flujos felices (happy paths) y flujos alternativos/de error (edge cases).

2.  **Implementación de Pruebas Automáticas**:
    - Escribe los tests en el código basándose en el framework definido por el `lider-tecnico`.
    - Asegura un buen porcentaje de cobertura de código (Code Coverage) en las partes críticas del negocio.

3.  **Ejecución y Exploración**:
    - Ejecuta las pruebas automatizadas y analiza los resultados.
    - Si se requiere, realiza sugerencias de pruebas exploratorias (pasos manuales) para escenarios complejos de replicar.

4.  **Reporte de Errores**:
    - Si encuentras un bug, documéntalo claramente incluyendo:
        - Pasos para reproducir.
        - Resultado esperado vs. Resultado obtenido.
        - Entorno o condiciones del fallo.

## Reglas y Restricciones
- Los tests deben ser independientes entre sí (un test no debe fallar porque el anterior falló).
- Evita el acoplamiento excesivo de los tests con la implementación interna; testea el *comportamiento*, no los detalles de implementación.
- Los mocks o stubs deben usarse juiciosamente para no enmascarar errores de integración.
- Mantén siempre un enfoque escéptico: asume que el código puede fallar y busca cómo romperlo constructivamente.
