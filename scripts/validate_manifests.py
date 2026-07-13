#!/usr/bin/env python3
"""CI gate: manifest hygiene that Cowork's server-side validation enforces.

1. hooks.json may contain ONLY documented fields (Cowork rejects unknown
   fields like $schema with status=failed_content -> the app shows a generic
   "Marketplace sync failed"). See docs/TROUBLESHOOTING.md section 4.
2. marketplace.json plugin versions must equal each plugin.json version --
   version pinning means users only get updates when the string changes, so
   the two must be bumped together. See docs/TROUBLESHOOTING.md section 2.
"""
import glob
import json
import sys

failures = []

# --- 1. hooks.json: documented fields only ---------------------------------
TOP_OK = {"hooks", "description"}
MATCHER_OK = {"matcher", "hooks"}
HOOK_OK = {"type", "command", "timeout"}
for path in glob.glob("plugins/*/hooks/hooks.json"):
    h = json.load(open(path))
    if "hooks" not in h:
        failures.append(f"{path}: missing 'hooks' key")
        continue
    unknown = set(h) - TOP_OK
    if unknown:
        failures.append(f"{path}: unknown top-level field(s) {sorted(unknown)} "
                        f"- Cowork remote validation rejects these")
    for event, matchers in h["hooks"].items():
        for m in matchers:
            bad = set(m) - MATCHER_OK
            if bad:
                failures.append(f"{path} [{event}]: unknown matcher field(s) {sorted(bad)}")
            for hk in m.get("hooks", []):
                bad = set(hk) - HOOK_OK
                if bad:
                    failures.append(f"{path} [{event}]: unknown hook field(s) {sorted(bad)}")
    print(f"{path}: hooks fields OK")

# --- 2. version consistency -------------------------------------------------
m = json.load(open(".claude-plugin/marketplace.json"))
for entry in m["plugins"]:
    pj_path = f"{entry['source']}/.claude-plugin/plugin.json"
    pj = json.load(open(pj_path))
    mv, pv = entry.get("version"), pj.get("version")
    if mv is not None and mv != pv:
        failures.append(f"{entry['name']}: marketplace.json version={mv} != "
                        f"plugin.json version={pv} - bump BOTH on every release")
    else:
        print(f"{entry['name']}: version {pv} consistent")

if failures:
    print("\nMANIFEST VALIDATION FAILED:")
    for f in failures:
        print(" -", f)
    sys.exit(1)
print("all manifest checks passed")
