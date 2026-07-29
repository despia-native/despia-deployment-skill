#!/usr/bin/env python3
"""Validate the skill against every channel that ships it.

One repo feeds three consumers: the Claude Code plugin marketplace, SkillUse,
and anyone copying the folder by hand. They all read the same commit, so a
malformed manifest or an over-long description breaks all of them at once and
silently. This runs on every push so that never reaches main.

Exits non-zero on the first failing check so CI goes red.
"""

import glob
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESCRIPTION_LIMIT = 1024  # Agent Skills spec / Claude Code frontmatter limit

failures = []
checks = 0


def check(condition, label):
    global checks
    checks += 1
    print(("  ok   " if condition else "  FAIL ") + label)
    if not condition:
        failures.append(label)


def parse_frontmatter(text):
    """Minimal YAML frontmatter reader - avoids a PyYAML dependency in CI."""
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    body = text[3:end]
    fields, key = {}, None
    for line in body.splitlines():
        if not line.strip():
            continue
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            key = m.group(1)
            fields[key] = m.group(2).strip()
        elif key and line.startswith((" ", "\t")):
            fields[key] += " " + line.strip()
    return fields


os.chdir(REPO)

print("MARKETPLACE")
mp_path = ".claude-plugin/marketplace.json"
check(os.path.isfile(mp_path), "marketplace.json exists")
if failures:
    sys.exit(1)
mp = json.load(open(mp_path))
check(bool(mp.get("name")), "marketplace has a name")
check(bool(mp.get("owner", {}).get("name")), "marketplace has an owner name")
check(isinstance(mp.get("plugins"), list) and mp["plugins"], "marketplace lists plugins")

for entry in mp["plugins"]:
    name = entry.get("name")
    source = entry.get("source", "")
    print(f"\nPLUGIN: {name}")
    check(bool(name), "plugin entry has a name")
    check(
        isinstance(source, str) and source.startswith("./") and os.path.isdir(source),
        f"source resolves to a directory: {source}",
    )
    if not os.path.isdir(source):
        continue

    manifest_path = os.path.join(source, ".claude-plugin", "plugin.json")
    check(os.path.isfile(manifest_path), "plugin.json exists")
    if os.path.isfile(manifest_path):
        manifest = json.load(open(manifest_path))
        check(manifest.get("name") == name, "plugin.json name matches marketplace entry")

    # Claude Code discovers plugin skills under <plugin>/skills/<skill>/SKILL.md.
    # SkillUse scans the git tree for any path ending in /SKILL.md, so this
    # layout satisfies both without duplicating the content.
    skill_dirs = sorted(glob.glob(os.path.join(source, "skills", "*")))
    check(bool(skill_dirs), "plugin has at least one skill")

    for skill_dir in skill_dirs:
        skill_name = os.path.basename(skill_dir)
        skill_md = os.path.join(skill_dir, "SKILL.md")
        print(f"\nSKILL: {skill_name}")
        check(os.path.isfile(skill_md), "SKILL.md present")
        if not os.path.isfile(skill_md):
            continue

        text = open(skill_md).read()
        fm = parse_frontmatter(text)
        check(fm is not None, "frontmatter parses")
        if fm is None:
            continue
        check("name" in fm, "frontmatter has name")
        check("description" in fm, "frontmatter has description")
        check(
            fm.get("name") == skill_name,
            f"frontmatter name matches directory ({fm.get('name')} vs {skill_name})",
        )
        desc = fm.get("description", "")
        check(
            len(desc) <= DESCRIPTION_LIMIT,
            f"description {len(desc)} chars <= {DESCRIPTION_LIMIT}",
        )

        ref_dir = os.path.join(skill_dir, "references")
        present = {os.path.basename(p) for p in glob.glob(os.path.join(ref_dir, "*.md"))}
        cited = set()
        for path in [skill_md] + sorted(glob.glob(os.path.join(ref_dir, "*.md"))):
            cited |= set(re.findall(r"references/([a-z0-9-]+\.md)", open(path).read()))
        missing = cited - present
        orphans = present - cited
        check(not missing, f"every cited reference exists{'' if not missing else f' - missing {sorted(missing)}'}")
        check(not orphans, f"every reference is cited{'' if not orphans else f' - orphaned {sorted(orphans)}'}")

print("\nREPO")
check(os.path.isfile("LICENSE"), "LICENSE present")
check(os.path.isfile("README.md"), "README present")

print(f"\n{checks - len(failures)}/{checks} checks passed")
if failures:
    print("\nFAILED:")
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)
print("Skill is valid for every publishing channel.")
