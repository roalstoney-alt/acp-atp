# Negative Results

## NR-0001 - Git baseline commit unavailable

`git status --short` and `git rev-parse HEAD` failed because the workspace is not a Git repository. The baseline cannot include a commit hash.

Impact: The Day-1 baseline relies on file hashes, test output, and explicit inventory rather than Git commit immutability.

## NR-0002 - Dependency-backed framework integration not completed

Common local agent framework packages were not installed. The Phase 6 adapter demonstrates an isolated LangChain-style tool-call boundary but does not prove integration against an installed framework package.

Impact: External integration evidence remains EML-2, not EML-5.

## NR-0003 - External reproduction not yet attempted

All reproduction in this run is internal. No external reviewer has completed the package.

Impact: Reproducibility remains internally reproduced only.
