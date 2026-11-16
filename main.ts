// Koi Leap — make.fun ai-excited-01 entry.
//
// One job, done carefully: take the artwork bundled in this repo
// (entry.jpg — a giant rainbow koi leaping over a neon city at dusk,
// an orange astronaut riding on its back) and drop an exact copy at the
// path the grader reads, $MAKEFUN_OUTPUT_DIR/entry.png.
//
// Node 22, standard library only. No network, no dependencies, no
// randomness — the same input bytes always produce the same output bytes.
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { createHash } from 'node:crypto';
import { copyFileSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ARTWORK_FILE = 'entry.jpg';
const OUTPUT_FILE = 'entry.png';
const DEFAULT_OUTPUT_DIR = '/output';

/** Where this script lives on disk, so the artwork is found beside it. */
function scriptDir(): string {
  return dirname(fileURLToPath(import.meta.url));
}

/** SHA-256 hex digest of a file's bytes. */
function sha256Hex(path: string): string {
  return createHash('sha256').update(readFileSync(path)).digest('hex');
}

/** Copy the artwork to the output directory and prove it landed intact. */
function deliverArtwork(): void {
  const sourcePath = resolve(scriptDir(), ARTWORK_FILE);
  const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? DEFAULT_OUTPUT_DIR;
  const targetPath = resolve(outputDir, OUTPUT_FILE);

  mkdirSync(outputDir, { recursive: true });
  copyFileSync(sourcePath, targetPath);

  // A short or corrupted copy must blow up loudly instead of silently
  // shipping a broken image to the judge. Check size first (cheap), then
  // the full SHA-256 digest (conclusive).
  const sourceBytes = statSync(sourcePath).size;
  const targetBytes = statSync(targetPath).size;
  if (sourceBytes !== targetBytes) {
    throw new Error(
      `Koi Leap: ${OUTPUT_FILE} size mismatch (${targetBytes} bytes copied, expected ${sourceBytes})`,
    );
  }
  const sourceHash = sha256Hex(sourcePath);
  const targetHash = sha256Hex(targetPath);
  if (sourceHash !== targetHash) {
    throw new Error(
      `Koi Leap: ${OUTPUT_FILE} failed integrity check ` +
        `(source ${sourceHash.slice(0, 12)}… vs copy ${targetHash.slice(0, 12)}…)`,
    );
  }

  console.log(`Koi Leap: wrote ${targetPath} (${targetBytes} bytes, sha256 ${sourceHash.slice(0, 12)}…)`);
}

deliverArtwork();
