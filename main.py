#!/usr/bin/env python3
"""news-23 b123 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only (no PIL). Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
Validates the source PNG first (signature, IHDR, chunk CRCs, IEND, size limits),
then copies it byte-for-byte and re-reads the output to confirm it is identical.
"""
import hashlib
import os
import struct
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
MIN_BYTES = 10_000
MAX_BYTES = 1_048_576
WANT_W, WANT_H = 1024, 1024


def fail(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def validate_png(data):
    if len(data) < MIN_BYTES:
        fail(f"entry.png too small: {len(data)} bytes (min {MIN_BYTES})")
    if len(data) > MAX_BYTES:
        fail(f"entry.png too big: {len(data)} bytes (max {MAX_BYTES})")
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        fail("bad PNG signature")
    # First chunk must be a 13-byte IHDR starting at offset 8:
    # signature(8) + length(4) + type(4) + data(13) + CRC(4) = 33 bytes,
    # so the next chunk starts at offset 33 (not 37: the 4-byte length field
    # is part of the 8-byte chunk header, not an extra prefix).
    length, ctype = struct.unpack(">I4s", data[8:16])
    if ctype != b"IHDR" or length != 13:
        fail("first chunk is not a 13-byte IHDR")
    ihdr = data[16:29]
    w, h, depth, ctype_b, comp, filt, inter = struct.unpack(">IIBBBBB", ihdr)
    if (w, h) != (WANT_W, WANT_H):
        fail(f"wrong dimensions: {w}x{h} (want {WANT_W}x{WANT_H})")
    if depth != 8 or ctype_b not in (2, 6):
        fail(f"unsupported IHDR: bit depth {depth}, colour type {ctype_b}")
    if comp != 0 or filt != 0 or inter != 0:
        fail("IHDR compression/filter/interlace must all be 0")
    crc_stored, = struct.unpack(">I", data[29:33])
    if zlib.crc32(b"IHDR" + ihdr) & 0xFFFFFFFF != crc_stored:
        fail("IHDR CRC mismatch")
    # Walk the remaining chunks: length + type + data + CRC each.
    off = 33
    idat_total = 0
    saw_iend = False
    while True:
        if off + 8 > len(data):
            fail("truncated chunk header")
        clen, ctype = struct.unpack(">I4s", data[off:off + 8])
        if off + 12 + clen > len(data):
            fail(f"truncated chunk {ctype!r}")
        chunk = data[off + 8:off + 8 + clen]
        crc_stored, = struct.unpack(">I", data[off + 8 + clen:off + 12 + clen])
        if zlib.crc32(ctype + chunk) & 0xFFFFFFFF != crc_stored:
            fail(f"CRC mismatch in chunk {ctype!r}")
        if ctype == b"IDAT":
            if clen == 0:
                fail("empty IDAT chunk")
            idat_total += clen
        if ctype == b"IEND":
            if clen != 0:
                fail("IEND must be 0 bytes")
            if off + 12 != len(data):
                fail("trailing data after IEND")
            saw_iend = True
            break
        off += 12 + clen
    if not saw_iend:
        fail("missing IEND chunk")
    if idat_total < 1000:
        fail(f"IDAT payload too small: {idat_total} bytes")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir_abs = os.path.abspath(out_dir)
    if os.path.isfile(out_dir_abs):
        fail(f"MAKEFUN_OUTPUT_DIR is a file: {out_dir}")
    if os.path.commonpath([out_dir_abs, HERE]) == HERE:
        fail("MAKEFUN_OUTPUT_DIR must not be inside the repository")
    dst = os.path.join(out_dir_abs, "entry.png")
    if os.path.abspath(dst) == os.path.abspath(SRC):
        fail("output would overwrite the source entry.png")
    try:
        with open(SRC, "rb") as f:
            data = f.read()
    except OSError as e:
        fail(f"cannot read entry.png: {e}")
    validate_png(data)
    os.makedirs(out_dir_abs, exist_ok=True)
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        written = f.read()
    if written != data:
        fail("output does not match source byte-for-byte")
    sha = hashlib.sha256(data).hexdigest()
    print(f"wrote {dst} ({len(data)} bytes, sha256 {sha})")


if __name__ == "__main__":
    main()
