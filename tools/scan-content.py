"""Quét nội dung công khai: không chép nguyên văn từ RFP / spec LAB-4, không email thật, không khóa bí mật.

Đối tượng quét: file văn bản trong repo + tiêu đề / body issue sinh từ backlog.yaml (đúng nội dung đẩy lên GitHub).
Chép nguyên văn = đoạn ≥ WINDOW ký tự (sau khi bỏ mã SCR-/API-/DBT-/WU-…, gộp khoảng trắng, chữ thường)
trùng với file nguồn (specs/**/*.md|yaml|mmd, input/rfp*.md của repo product-a-fishmarket).
Mã được phép ghi nên bị loại trước khi so.

Chạy:  python tools/scan-content.py [--source PATH_TO_product-a-fishmarket]
"""
import re
import sys
from pathlib import Path

import backlog_model as bm

WINDOW = 40
REPO_ROOT = bm.TOOLS_DIR.parent
DEFAULT_SOURCE = REPO_ROOT.parent / "product-a-fishmarket"
TEXT_EXT = {".md", ".yaml", ".yml", ".py", ".sh", ".json", ".txt"}
CODE_ID = re.compile(r"\b[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+(?:〜[0-9]+)?\b|\bD\d{1,2}\b|#\d+")
SECRETS = {
    "email": re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+"),
    "github token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_\w{20,})"),
    "aws key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "api key": re.compile(r"\b(?:sk|pk)-[A-Za-z0-9]{20,}"),
    "password": re.compile(r"(?i)\b(?:password|passwd|secret)\s*[:=]\s*['\"][^'\"]{4,}"),
}
ALLOWED_EMAIL = re.compile(r"@users\.noreply\.github\.com$|@example\.(?:com|org)$")


def normalize(text):
    return re.sub(r"\s+", " ", CODE_ID.sub(" ", text)).lower()


def targets():
    """(tên, nội dung) của mọi văn bản sẽ công khai."""
    out = []
    for p in sorted(REPO_ROOT.rglob("*")):
        rel = p.relative_to(REPO_ROOT).as_posix()
        if p.is_file() and p.suffix in TEXT_EXT and not rel.startswith((".git/", ".claude/", "plans/")):
            out.append((rel, p.read_text(encoding="utf-8", errors="replace")))
    meta, items, by_id = bm.load()
    for it in items:
        out.append((f"issue {it.id}", it.title + "\n" + bm.render_body(it, by_id, meta, {})))
    return out


def corpus_files(source):
    files = [p for p in (source / "specs").rglob("*") if p.suffix in {".md", ".yaml", ".yml", ".mmd"}]
    files += sorted((source / "input").glob("rfp*.md"))
    return files


def scan_copy(source):
    docs = [(name, normalize(text)) for name, text in targets()]
    index = {}
    for di, (_, t) in enumerate(docs):
        for i in range(len(t) - WINDOW + 1):
            index.setdefault(t[i:i + WINDOW], []).append((di, i))
    hits = {}
    for f in corpus_files(source):
        t = normalize(f.read_text(encoding="utf-8", errors="replace"))
        for i in range(len(t) - WINDOW + 1):
            for di, pos in index.get(t[i:i + WINDOW], ()):
                hits.setdefault(di, set()).add(pos)
    findings = []
    for di, positions in hits.items():
        name, t = docs[di]
        for start, end in _spans(sorted(positions)):
            snippet = t[start:end + WINDOW].strip()
            if re.search(r"[a-zà-ỹ぀-ヿ一-鿿]{3}", snippet):  # bỏ đoạn chỉ có ký hiệu / số
                findings.append((name, snippet))
    return findings


def _spans(positions):
    start = prev = positions[0]
    for p in positions[1:]:
        if p != prev + 1:
            yield start, prev
            start = p
        prev = p
    yield start, prev


def scan_secrets():
    found = []
    for name, text in targets():
        for kind, rx in SECRETS.items():
            for m in rx.finditer(text):
                if kind == "email" and ALLOWED_EMAIL.search(m.group(0)):
                    continue
                found.append((name, kind, m.group(0)[:60]))
    return found


def main():
    args = sys.argv[1:]
    source = Path(args[args.index("--source") + 1]) if "--source" in args else DEFAULT_SOURCE
    copies = scan_copy(source) if source.exists() else None
    secrets = scan_secrets()
    if copies is None:
        print(f"BỎ QUA quét chép: không thấy {source}")
    for name, snippet in copies or []:
        print(f"✗ trùng nguồn ({len(snippet)} ký tự) ở {name}: «{snippet[:120]}»")
    for name, kind, val in secrets:
        print(f"✗ {kind} ở {name}: {val}")
    n = len(copies or []) + len(secrets)
    print(f"KẾT QUẢ: {'ĐẠT' if n == 0 else f'{n} phát hiện'} (cửa sổ {WINDOW} ký tự, {len(targets())} văn bản)")
    sys.exit(1 if n else 0)


if __name__ == "__main__":
    main()
