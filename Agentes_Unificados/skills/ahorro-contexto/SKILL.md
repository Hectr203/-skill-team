---
name: ahorro-contexto
description: Use this skill when working in this project to reduce token usage, avoid unnecessary context loading, minimize memory usage, and keep project work concise and efficient.
---

# Ahorro de contexto y tokens

When working in this project:

- Do not read large files unless necessary.
- Do not scan the whole repository unless the task requires it.
- Prefer targeted searches over broad searches.
- Read only the files directly related to the task.
- Summarize findings briefly.
- Avoid repeating file contents unless requested.
- Avoid loading generated folders, dependency folders, build outputs, cache folders, logs, and binary files.
- Before editing, identify the smallest set of files needed.
- Prefer small, focused changes.
- Do not create long explanations after code changes.
- Do not include large diffs in the response unless requested.
- Mention only changed files and the reason for each change.
- Keep answers short and practical.

Avoid reading or indexing these paths unless explicitly requested:

- node_modules/
- vendor/
- dist/
- build/
- coverage/
- .git/
- .cache/
- .next/
- .nuxt/
- out/
- target/
- tmp/
- logs/
- *.log
- *.lock
- package-lock.json
- yarn.lock
- pnpm-lock.yaml
- composer.lock

Default workflow:

1. Understand the request.
2. Search only relevant filenames, symbols, or folders.
3. Open the smallest useful files.
4. Make the minimal necessary change.
5. Respond with a short summary.
