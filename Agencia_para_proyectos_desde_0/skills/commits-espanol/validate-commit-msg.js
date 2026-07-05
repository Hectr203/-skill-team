#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Read the commit message from the file passed by Git
const commitMsgFile = process.argv[2];
if (!commitMsgFile) {
  console.error('Error: No se proporcionó el archivo del mensaje de commit.');
  process.exit(1);
}

let commitMsg = '';
try {
  commitMsg = fs.readFileSync(commitMsgFile, 'utf8');
} catch (err) {
  console.error('Error al leer el archivo del mensaje de commit:', err.message);
  process.exit(1);
}

// Clean comments (lines starting with #) and get non-empty lines
const lines = commitMsg.split('\n')
  .map(line => line.trim())
  .filter(line => line.length > 0 && !line.startsWith('#'));

if (lines.length === 0) {
  // Empty commit message, let Git handle it
  process.exit(0);
}

const subjectLine = lines[0];

// Allow merge, revert, squash, fixup commits
if (
  /^(Merge |Revert |squash!|fixup!)/i.test(subjectLine) ||
  subjectLine.startsWith('Merge branch') ||
  subjectLine.startsWith('Merge pull request')
) {
  process.exit(0);
}

// Extract description (the part after the conventional commits prefix, if any)
let description = subjectLine;
const colonIndex = subjectLine.indexOf(':');
if (colonIndex !== -1) {
  description = subjectLine.substring(colonIndex + 1).trim();
}

// Get the first word of the description
const words = description.split(/\s+/).filter(w => w.length > 0);
if (words.length === 0) {
  process.exit(0);
}

const firstWord = words[0].toLowerCase().replace(/[^a-z]/g, '');

// List of common English git commit verbs that are blocked
const blockedVerbs = {
  'add': 'agrega, crea o implementa',
  'added': 'agrega, crea o implementa',
  'adding': 'agrega, crea o implementa',
  'adds': 'agrega, crea o implementa',
  'fix': 'corrige o soluciona',
  'fixed': 'corrige o soluciona',
  'fixing': 'corrige o soluciona',
  'fixes': 'corrige o soluciona',
  'update': 'actualiza o modifica',
  'updated': 'actualiza o modifica',
  'updating': 'actualiza o modifica',
  'updates': 'actualiza o modifica',
  'delete': 'elimina o quita',
  'deleted': 'elimina o quita',
  'deleting': 'elimina o quita',
  'deletes': 'elimina o quita',
  'remove': 'elimina o quita',
  'removed': 'elimina o quita',
  'removing': 'elimina o quita',
  'removes': 'elimina o quita',
  'create': 'crea, agrega o implementa',
  'created': 'crea, agrega o implementa',
  'creating': 'crea, agrega o implementa',
  'creates': 'crea, agrega o implementa',
  'implement': 'implementa o crea',
  'implemented': 'implementa o crea',
  'implementing': 'implementa o crea',
  'implements': 'implementa o crea',
  'refactor': 'refactoriza o reestructura',
  'refactored': 'refactoriza o reestructura',
  'refactoring': 'refactoriza o reestructura',
  'refactors': 'refactoriza o reestructura',
  'change': 'cambia o modifica',
  'changed': 'cambia o modifica',
  'changing': 'cambia o modifica',
  'changes': 'cambia o modifica',
  'make': 'hace o crea',
  'made': 'hace o crea',
  'making': 'hace o crea',
  'makes': 'hace o crea',
  'setup': 'configura o inicializa',
  'setup/set': 'configura o inicializa',
  'set': 'configura o establece',
  'build': 'construye o compila',
  'built': 'construye o compila',
  'building': 'construye o compila',
  'builds': 'construye o compila',
  'test': 'prueba o añade tests',
  'tested': 'prueba o añade tests',
  'testing': 'prueba o añade tests',
  'tests': 'prueba o añade tests',
  'clean': 'limpia o depura',
  'cleaned': 'limpia o depura',
  'cleaning': 'limpia o depura',
  'cleans': 'limpia o depura',
  'adjust': 'ajusta o modifica',
  'adjusted': 'ajusta o modifica',
  'adjusting': 'ajusta o modifica',
  'adjusts': 'ajusta o modifica',
  'improve': 'mejora o perfecciona',
  'improved': 'mejora o perfecciona',
  'improving': 'mejora o perfecciona',
  'improves': 'mejora o perfecciona',
  'integrate': 'integra o une',
  'integrated': 'integra o une',
  'integrating': 'integra o une',
  'integrates': 'integra o une',
  'handle': 'maneja, gestiona o trata',
  'handled': 'maneja, gestiona o trata',
  'handling': 'maneja, gestiona o trata',
  'handles': 'maneja, gestiona o trata',
  'allow': 'permite o habilita',
  'allowed': 'permite o habilita',
  'allowing': 'permite o habilita',
  'allows': 'permite o habilita',
  'enable': 'habilita o activa',
  'enabled': 'habilita o activa',
  'enabling': 'habilita o activa',
  'enables': 'habilita o activa',
  'disable': 'deshabilita o desactiva',
  'disabled': 'deshabilita o desactiva',
  'disabling': 'deshabilita o desactiva',
  'disables': 'deshabilita o desactiva',
  'show': 'muestra o visualiza',
  'showed': 'muestra o visualiza',
  'showing': 'muestra o visualiza',
  'shows': 'muestra o visualiza',
  'hide': 'oculta o esconde',
  'hid': 'oculta o esconde',
  'hiding': 'oculta o esconde',
  'hides': 'oculta o esconde',
  'use': 'usa o utiliza',
  'used': 'usa o utiliza',
  'using': 'usa o utiliza',
  'uses': 'usa o utiliza',
  'require': 'requiere o necesita',
  'required': 'requiere o necesita',
  'requiring': 'requiere o necesita',
  'requires': 'requiere o necesita',
  'move': 'mueve o traslada',
  'moved': 'mueve o traslada',
  'moving': 'mueve o traslada',
  'moves': 'mueve o traslada',
  'document': 'documenta o registra',
  'documented': 'documenta o registra',
  'documenting': 'documenta o registra',
  'documents': 'documenta o registra'
};

if (blockedVerbs.hasOwnProperty(firstWord)) {
  const suggestion = blockedVerbs[firstWord];
  console.error('\x1b[31m%s\x1b[0m', '========================================================================');
  console.error('\x1b[31m%s\x1b[0m', ' ERROR DE COMMIT: Regla Global de Mensajes en Español (commits-espanol) ');
  console.error('\x1b[31m%s\x1b[0m', '========================================================================');
  console.error(`El mensaje de commit debe estar redactado en español.`);
  console.error(`Se detectó que el mensaje o su descripción inicia con el verbo en inglés: "${words[0]}"`);
  console.error(`\nPor favor, utiliza verbos en español. Sugerencia para "${words[0]}": usar "${suggestion}".`);
  console.error('\nEjemplos correctos:');
  console.error('  feat: agrega panel de control');
  console.error('  fix: corrige error de validación de formulario');
  console.error('  docs: actualiza manual de usuario');
  console.error('\x1b[31m%s\x1b[0m', '========================================================================');
  console.error(`Tu mensaje original era:\n"${subjectLine}"\n`);
  process.exit(1);
}

// Check for common English stop words to detect a full English description
const englishStopWords = new Set(['the', 'with', 'for', 'and', 'from', 'into', 'about', 'some', 'any', 'all']);
const spanishStopWords = new Set(['el', 'la', 'los', 'las', 'un', 'una', 'con', 'para', 'y', 'de', 'del', 'al', 'en', 'por', 'sobre', 'algun', 'alguna', 'todos', 'todas']);

let englishWordCount = 0;
let spanishWordCount = 0;

for (const word of words) {
  const cleanWord = word.toLowerCase().replace(/[^a-zñáéíóúü]/g, '');
  if (englishStopWords.has(cleanWord)) englishWordCount++;
  if (spanishStopWords.has(cleanWord)) spanishWordCount++;
}

if (englishWordCount > 0 && spanishWordCount === 0) {
  console.error('\x1b[31m%s\x1b[0m', '========================================================================');
  console.error('\x1b[31m%s\x1b[0m', ' ERROR DE COMMIT: Regla Global de Mensajes en Español (commits-espanol) ');
  console.error('\x1b[31m%s\x1b[0m', '========================================================================');
  console.error(`El mensaje de commit parece estar redactado completamente en inglés.`);
  console.error(`Se detectaron palabras funcionales del inglés (ej. "the", "with", "for", "and").`);
  console.error(`\nPor favor, traduce la descripción del commit al español.`);
  console.error('\x1b[31m%s\x1b[0m', '========================================================================');
  console.error(`Tu mensaje original era:\n"${subjectLine}"\n`);
  process.exit(1);
}

process.exit(0);
