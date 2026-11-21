#!/usr/bin/env python3
"""Lumivere — travel poster for a place that isn't there.

Copies the poster image (entry.png, next to this file) into the grader's
output directory as entry.png, then checks the copy is a whole PNG.
Reads MAKEFUN_OUTPUT_DIR, falling back to /output.
"""

import os
import shutil
import struct
import sys

SOURCE_NAME = "entry.png"
OUTPUT_NAME = "entry.png"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)
    if not os.path.isfile(source):
        fail(f"source image not found: {source}")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, OUTPUT_NAME)

    shutil.copyfile(source, target)

    with open(target, "rb") as handle:
        head = handle.read(len(PNG_SIGNATURE))
    if head != PNG_SIGNATURE:
        fail(f"{target} is not a PNG file")

    size = os.path.getsize(target)
    if size > MAX_BYTES:
        fail(f"{target} is {size} bytes, over the {MAX_BYTES} byte limit")

    with open(target, "rb") as handle:
        header = handle.read(33)
    if len(header) < 33 or header[12:16] != b"IHDR":
        fail(f"{target} has no PNG IHDR chunk")
    width, height = struct.unpack(">II", header[16:24])
    if width > 1024 or height > 1024:
        fail(f"{target} is {width}x{height}, over the 1024x1024 limit")
    print(f"poster is {width}x{height}")

    with open(source, "rb") as handle:
        original = handle.read()
    with open(target, "rb") as handle:
        copied = handle.read()
    if copied != original:
        fail(f"{target} differs from {source} after the copy")

    print(f"wrote {target} ({size} bytes, verified byte-identical)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
