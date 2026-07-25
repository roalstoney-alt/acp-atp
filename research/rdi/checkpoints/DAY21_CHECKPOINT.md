# Day 21 Checkpoint

## Files Created And Modified

Created: `REPRODUCTION.md`, `integrations/`, `content/outreach/`, and crosswalk files.

## Test Results

`python3 -B -m integrations.selected_framework.demo`: passed expected decision sequence.

`python3 -B -m unittest discover -s tests`: 34 tests passed.

## Newly Verified Claims

- Adapter can gate a LangChain-style tool invocation boundary.
- Adapter demo records allow, confirmation, exact confirmation, revocation, undeclared tool, and evidence integrity.

## Failed Claims

- Dependency-backed external framework integration is not complete.

## EML Changes

- Adapter boundary compatibility is EML-2.
- External integration remains below EML-5.

## Known P0/P1 Risks

P1: no installed open framework dependency was available.

## Negative Results

Framework packages were absent locally.

## Next Gate Status

G5: PASS internal dry-run package.

G6: PARTIAL because adapter exists but dependency-backed integration remains unproven.

G7: PASS prepared-not-sent.
