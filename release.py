#!/usr/bin/env python3
"""
Release helper for modsync.

Usage:
    python release.py

Creates:
    - version update
    - release commit
    - git tag

Optionally pushes to origin.
"""

import re
import subprocess
import sys
from pathlib import Path

VERSION_FILE = Path("version.py")
VERSION_PATTERN = re.compile(r'__version__\s*=\s*"([^"]+)"')
SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")


def run(cmd):
    print(f"> {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


def git_output(cmd):
    return subprocess.check_output(cmd, text=True).strip()


def get_current_version():
    text = VERSION_FILE.read_text()

    match = VERSION_PATTERN.search(text)
    if not match:
        raise RuntimeError("Could not locate __version__ in version.py")

    return match.group(1)


def update_version(version):
    text = VERSION_FILE.read_text()

    text = VERSION_PATTERN.sub(
        f'__version__ = "{version}"',
        text,
    )

    VERSION_FILE.write_text(text)


def confirm(prompt, default=True):
    suffix = "[Y/n]" if default else "[y/N]"

    while True:
        response = input(f"{prompt} {suffix}: ").strip().lower()

        if response == "":
            return default

        if response in ("y", "yes"):
            return True

        if response in ("n", "no"):
            return False


def ensure_clean_git():
    status = git_output(["git", "status", "--porcelain"])

    if status:
        print("Your git working tree is not clean.")
        print("Please commit or stash your changes before releasing.")
        sys.exit(1)


def main():
    ensure_clean_git()

    current_version = get_current_version()

    print()
    print(f"Current version: {current_version}")
    print()

    while True:
        version = input("Enter new version: ").strip()

        if not SEMVER_PATTERN.match(version):
            print("Version must be in the format X.Y.Z")
            continue

        if version == current_version:
            print("Version is already current.")
            continue

        break

    print()
    print("Summary")
    print("-------")
    print(f"Current: {current_version}")
    print(f"New:     {version}")
    print()

    if not confirm("Proceed?"):
        print("Release cancelled.")
        return

    update_version(version)

    print()
    print("Updating version.py...")

    run(["git", "add", str(VERSION_FILE)])
    run(["git", "commit", "-m", f"Release v{version}"])
    run(["git", "tag", f"v{version}"])

    print()
    print("✓ Version updated")
    print("✓ Commit created")
    print(f"✓ Tag created: v{version}")

    print()

    if confirm("Push commit and tag to origin?", default=False):
        run(["git", "push"])
        run(["git", "push", "origin", f"v{version}"])

        print()
        print("Release published!")
        print("https://github.com/coltsaw/modsync/releases")
    else:
        print()
        print("Release prepared locally.")
        print()
        print("Run the following when you're ready:")
        print("  git push")
        print(f"  git push origin v{version}")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError:
        print("\nA git command failed. Release aborted.")
        sys.exit(1)