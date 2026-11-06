// Fails when any \( ... \) formula in the SAT questions cannot be typeset by KaTeX.
import { readFileSync } from 'node:fs';
import katex from 'katex';

const load = name => JSON.parse(readFileSync(new URL(`../data/${name}`, import.meta.url), 'utf8'));
const bank = [...load('sat_question_bank.json'), ...load('sat_math_practice.json')];
const FORMULA = /\\\((.+?)\\\)/gs;
let checked = 0;
const failures = [];

for (const question of bank) {
  const fields = [question.q, question.pas, question.exp, question.strat, ...(question.opts || [])];
  for (const text of fields) {
    for (const match of (text || '').matchAll(FORMULA)) {
      checked += 1;
      try {
        katex.renderToString(match[1], { throwOnError: true });
      } catch (error) {
        failures.push(`${question.id}: ${match[1]} (${error.message})`);
      }
    }
  }
}

console.log(`Checked ${checked} formulas, ${failures.length} failed.`);
failures.slice(0, 40).forEach(line => console.log(line));
process.exit(failures.length ? 1 : 0);
