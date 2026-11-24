"""Ship It Friday — entrypoint.

Writes one line to /output/entry.txt: the funniest git commit message
an AI coding agent would write right before breaking production on
a Friday. Standard library only (os, pathlib), so it runs on the
grader's stock python:3.13-slim image.
"""

import os
from pathlib import Path

ENTRY = "feat: ship to prod at 4:59pm Friday \u2014 rollback plan is vibes and a prayer"

MIN_LEN = 1
MAX_LEN = 159


def gate(text: str) -> None:
    """Enforce the competition gate: UTF-8 text, 1-159 chars, not
    only whitespace, exactly one line."""
    if not (MIN_LEN <= len(text) <= MAX_LEN):
        raise ValueError(f"entry length {len(text)} outside 1-159")
    if not text.strip():
        raise ValueError("entry is only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    text.encode("utf-8")


def main() -> None:
    gate(ENTRY)
    out_dir = Path(os.environ["MAKEFUN_OUTPUT_DIR"])
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    target.write_text(ENTRY, encoding="utf-8")
    # Byte-exact read-back: what the grader will see is exactly ENTRY,
    # with no trailing newline smuggled in by the write.
    raw = target.read_bytes()
    if raw != ENTRY.encode("utf-8"):
        raise ValueError("read-back mismatch")
    if raw.endswith(b"\n"):
        raise ValueError("entry must not end with a newline")
    print(f"wrote entry.txt ({len(ENTRY)} chars, {len(raw)} bytes)")


if __name__ == "__main__":
    main()
