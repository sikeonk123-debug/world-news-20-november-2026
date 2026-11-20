// Entry program for the make.fun bounty "Sum up 20 November's world news
// in one image" (news-image-20261120).
//
// The entry image is drawn by draw.py (Python + Pillow) and stored in this
// repository as entry.png. This program copies it to the output directory
// the harness gives us, validating that it stays within the 1 MiB limit.
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const entry = readFileSync(new URL("./entry.png", import.meta.url));
if (entry.length > 1024 * 1024) {
  throw new Error(`entry.png is ${entry.length} bytes, over the 1 MiB limit`);
}
mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, "entry.png"), entry);
console.log(`wrote ${join(outDir, "entry.png")} (${entry.length} bytes)`);
