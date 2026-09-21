---
name: ponytail
description: Use before implementing to choose the smallest correct solution, avoid unnecessary dependencies and preserve security, accessibility and tests.
---
# Ponytail
Use the first applicable rung: YAGNI, standard library, native platform, existing dependency, one clear line, then minimum new code. Never use it to remove trust-boundary validation, error handling, accessibility or required tests. Record intentional ceilings with `ponytail:` comments. Every non-trivial change leaves one runnable check.
