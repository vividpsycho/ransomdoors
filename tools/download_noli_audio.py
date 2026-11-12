#!/usr/bin/env python3
"""Download every audio file linked from the JX1DX1 Noli scrapped-skin page."""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API = "https://forsaken2024.fandom.com/api.php"
PAGE = "Noli/Skins/Scrapped"
OUTPUT = Path("Assets/Sounds/Noli")
AUDIO_EXTENSIONS = {".mp3", ".ogg", ".oga", ".wav"}


def api(params: dict[str, str]) -> dict:
    request = Request(
        API + "?" + urlencode(params),
        headers={"User-Agent": "ransomdoors-audio-asset-fetcher/1.0 (GitHub Actions)"},
    )
    with urlopen(request, timeout=45) as response:
        return json.load(response)


def main() -> int:
    print(f"Reading file links from {PAGE}")
    parsed = api({
        "action": "parse", "page": PAGE, "prop": "links",
        "plnamespace": "6", "pllimit": "max", "format": "json",
        "formatversion": "2",
    })
    links = parsed.get("parse", {}).get("links", [])
    names = sorted({
        item["title"].removeprefix("File:")
        for item in links
        if item.get("title", "").startswith("File:")
        and Path(item["title"].removeprefix("File:")).suffix.lower() in AUDIO_EXTENSIONS
    })
    if not names:
        print("No audio file links were returned by the wiki API.", file=sys.stderr)
        return 1

    OUTPUT.mkdir(parents=True, exist_ok=True)
    downloaded = skipped = failed = 0
    for name in names:
        target = OUTPUT / name.replace("/", "_").replace(" ", "_")
        if target.exists() and target.stat().st_size:
            skipped += 1
            continue
        try:
            result = api({
                "action": "query", "titles": "File:" + name,
                "prop": "imageinfo", "iiprop": "url",
                "format": "json", "formatversion": "2",
            })
            pages = result.get("query", {}).get("pages", [])
            info = pages[0].get("imageinfo", []) if pages else []
            if not info:
                raise RuntimeError("no downloadable URL returned")
            request = Request(
                info[0]["url"],
                headers={"User-Agent": "ransomdoors-audio-asset-fetcher/1.0"},
            )
            with urlopen(request, timeout=90) as response:
                data = response.read()
            if not data:
                raise RuntimeError("empty response")
            target.write_bytes(data)
            downloaded += 1
            print(f"Downloaded {target.name} ({len(data):,} bytes)")
            time.sleep(0.2)
        except (HTTPError, URLError, KeyError, IndexError, RuntimeError, TimeoutError) as exc:
            failed += 1
            print(f"FAILED {name}: {exc}", file=sys.stderr)

    print(f"\nResult: {downloaded} downloaded, {skipped} already present, {failed} failed.")
    print(f"Output: {OUTPUT}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
