"""Cài skill cho Claude Code: copy skills/swp-provisional/ → .claude/skills/swp-provisional/ của repo.

Nguồn chuẩn là skills/ (được commit); bản ở .claude/ chỉ là bản cài, bị .gitignore, chạy lại sẽ ghi đè.
Chạy:  python skills/swp-provisional/scripts/install-skill.py
"""
import shutil
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):  # Windows: stdout chuyển hướng mặc định code page ANSI
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

SKILL_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = SKILL_DIR.parent.parent
TARGET = REPO_ROOT / ".claude" / "skills" / SKILL_DIR.name


def main():
    if TARGET.exists():
        shutil.rmtree(TARGET)
    shutil.copytree(SKILL_DIR, TARGET, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    files = sorted(p.relative_to(TARGET).as_posix() for p in TARGET.rglob("*") if p.is_file())
    print(f"Đã cài {len(files)} file → {TARGET}")
    for f in files:
        print("  ", f)


if __name__ == "__main__":
    main()
