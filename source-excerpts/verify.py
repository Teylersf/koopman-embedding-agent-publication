"""Verify selective quotations against the exact public arXiv source archive."""

import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import tarfile


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()
    folder = Path(__file__).resolve().parent
    manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    archive = args.archive.read_bytes()
    expected_archive = manifest["source_archive"]
    if len(archive) != expected_archive["bytes"] or sha256(archive) != expected_archive["sha256"]:
        raise SystemExit("Archive bytes/hash differ from the checked versioned artifact.")
    expected_source = manifest["source_file"]
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:*") as handle:
        candidates = [member for member in handle.getmembers()
                      if member.isfile() and PurePosixPath(member.name).name == expected_source["name"]]
        if len(candidates) != 1:
            raise SystemExit("Expected exactly one regular Limit.tex member.")
        member = candidates[0]
        if member.size != expected_source["bytes"]:
            raise SystemExit("Original source length differs.")
        source = handle.extractfile(member).read()
    if sha256(source) != expected_source["sha256"]:
        raise SystemExit("Original source hash differs.")
    lines = source.decode("utf-8").splitlines()
    checked = 0
    for entry in manifest["excerpts"]:
        payload = (folder / entry["file"]).read_bytes()
        if sha256(payload) != entry["sha256"]:
            raise SystemExit(f"Excerpt-file hash differs: {entry['file']}")
        expected_lines = []
        for index, (start, end) in enumerate(entry["source_line_ranges"]):
            if index:
                expected_lines.append("[noncontiguous source ranges; intervening text omitted]")
            expected_lines.extend(f"{number}: {lines[number - 1]}" for number in range(start, end + 1))
            checked += end - start + 1
        actual = payload.decode("utf-8").split("--- BEGIN LINE-NUMBERED EXCERPT ---\n", 1)[1]
        if actual != "\n".join(expected_lines) + "\n":
            raise SystemExit(f"Original source-line mismatch: {entry['file']}")
    print(f"PASS: exact archive, Limit.tex and {len(manifest['excerpts'])} excerpts ({checked} source lines).")


if __name__ == "__main__":
    main()
