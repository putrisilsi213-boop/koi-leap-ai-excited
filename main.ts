// Koi Leap — make.fun ai-excited-01.
//
// This program has exactly one responsibility: take the artwork that
// ships in this repository (entry.jpg — a rainbow koi leaping over a
// neon city at dusk with an orange astronaut riding on its back) and
// place a byte-identical copy where the grader looks for it:
// $MAKEFUN_OUTPUT_DIR/entry.png.
//
// It uses Node 22's standard library and nothing else: no packages,
// no network, no randomness. Given the same entry.jpg it always
// produces the same entry.png.
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { createHash } from 'node:crypto';
import { copyFileSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ARTWORK = 'entry.jpg';
const OUTPUT_NAME = 'entry.png';
const FALLBACK_DIR = '/output';

function here(): string {
  return dirname(fileURLToPath(import.meta.url));
}

function digest(path: string): string {
  return createHash('sha256').update(readFileSync(path)).digest('hex');
}

/** The artwork must be a real JPEG, not an empty or misnamed file. */
function assertJpeg(path: string): void {
  const head = readFileSync(path).subarray(0, 3);
  if (head[0] !== 0xff || head[1] !== 0xd8 || head[2] !== 0xff) {
    throw new Error(`Koi Leap: ${ARTWORK} does not start with a JPEG magic number`);
  }
}

function main(): void {
  const source = resolve(here(), ARTWORK);
  const dir = process.env.MAKEFUN_OUTPUT_DIR ?? FALLBACK_DIR;
  const dest = resolve(dir, OUTPUT_NAME);

  assertJpeg(source);
  mkdirSync(dir, { recursive: true });
  copyFileSync(source, dest);

  // Refuse to hand the judge a truncated or corrupted image: the copy
  // must match the original byte for byte, in size and in SHA-256.
  const expectedSize = statSync(source).size;
  const actualSize = statSync(dest).size;
  if (actualSize !== expectedSize) {
    throw new Error(
      `Koi Leap: ${OUTPUT_NAME} is ${actualSize} bytes, expected ${expectedSize}`,
    );
  }
  const expectedHash = digest(source);
  const actualHash = digest(dest);
  if (actualHash !== expectedHash) {
    throw new Error(
      `Koi Leap: ${OUTPUT_NAME} checksum mismatch ` +
        `(got ${actualHash.slice(0, 12)}…, want ${expectedHash.slice(0, 12)}…)`,
    );
  }

  console.log(
    `Koi Leap: ${dest} ready — ${actualSize} bytes, sha256 ${expectedHash.slice(0, 12)}…`,
  );
}

main();
