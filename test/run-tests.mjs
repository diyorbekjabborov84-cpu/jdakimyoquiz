import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import path from "node:path";

const projectRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const tsxCli = path.join(projectRoot, "node_modules", "tsx", "dist", "cli.mjs");
const allTestFiles = [
  "index.test.ts",
  "quiz.test.ts",
  "e2e-simulation.test.ts",
  "multi-quiz.test.ts",
  "subscription.test.ts",
  "kk1-quiz.test.ts",
  "kk2-quiz.test.ts",
  "russian-quiz.test.ts",
  "smart-pause-welcome.test.ts",
  "phase2-storage.test.ts",
  "firestore.test.ts",
];
const requested = process.argv.slice(2);
const testFiles = requested.length ? requested : allTestFiles;
if (testFiles.some((name) => !allTestFiles.includes(name))) {
  throw new Error("Unknown test file requested");
}

for (const testFile of testFiles) {
  const result = spawnSync(process.execPath, [tsxCli, path.join(projectRoot, "test", testFile)], {
    cwd: projectRoot,
    env: { ...process.env, NODE_ENV: "test", FIRESTORE_LOCAL_ENABLED: "false" },
    stdio: "inherit",
  });
  if (result.error) throw result.error;
  if (result.status !== 0) process.exit(result.status ?? 1);
}
