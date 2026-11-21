// Entry program for the make.fun bounty "Sum up 20 November's world news
// in one image" (news-image-20261120), final version (v3, 21 Nov 2026).
//
// The entry image is drawn by draw.py (Python 3 + Pillow) and stored in
// this repository as entry.png: a one-page newspaper front page with 35
// verified stories from Friday 20 November 2026. This program checks the
// image is a real 1024x1024 PNG under the 1 MiB limit and copies it to
// the output directory the harness gives us.
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const MAX_BYTES = 1024 * 1024;
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const entry = readFileSync(new URL("./entry.png", import.meta.url));

if (!entry.subarray(0, 8).equals(PNG_MAGIC)) {
  throw new Error("entry.png is not a PNG file");
}
// IHDR chunk: width and height are big-endian uint32 at offsets 16 and 20.
const width = entry.readUInt32BE(16);
const height = entry.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  throw new Error(`entry.png is ${width}x${height}, expected 1024x1024`);
}
if (entry.length > MAX_BYTES) {
  throw new Error(`entry.png is ${entry.length} bytes, over the 1 MiB limit`);
}

mkdirSync(outDir, { recursive: true });
const outPath = join(outDir, "entry.png");
writeFileSync(outPath, entry);
console.log(`wrote ${outPath} (${width}x${height}, ${entry.length} bytes)`);
