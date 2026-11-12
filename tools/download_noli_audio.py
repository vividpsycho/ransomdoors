#!/usr/bin/env python3
"""Download the JX1DX1/Noli audio files linked from the Forsaken Fandom page.

Run from the repository root:
    python tools/download_noli_audio.py

Files are saved under Assets/Sounds/Noli. Existing files are skipped.
"""
from __future__ import annotations

import json
import re
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
# Keep this focused on the JX1DX1 skin audio, including its unused/scrapped lines.
NAME_FILTER = re.compile(r"(?:JX1DX1|JX1|Jx1|Jxstun|The_laugher)", re.IGNORECASE)


def get_json(params: dict[str, str]) -> dict:
    url = API + "?" + urlencode(params)
    request = Request(url, headers={"User-Agent": "RansomdoorsAssetFetcher/1.0"})
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def main() -> int:
    print(f"Reading audio file list from: {PAGE}")
    page = get_json({
        "action": "parse",
        "page": PAGE,
        "prop": "wikitext",
        "format": "json",
    })
    wikitext = page.get("parse", {}).get("wikitext", {}).get("*", "")
    if not wikitext:
        print("Could not read the page wikitext. The wiki may be unavailable.", file=sys.stderr)
        return 1

    # Fandom's page links audio through File:... entries. Decode only audio files
    # associated with the JX1DX1 skin; do not scrape unrelated Noli recordings.
    names = set(re.findall(r"(?:File|Image):([^|\]#\n]+)", wikitext, re.IGNORECASE))
    names = {
        name.strip().replace("_", " ")
        for name in names
        if Path(name.strip().replace("_", " ")).suffix.lower() in AUDIO_EXTENSIONS
        and NAME_FILTER.search(name)
    }
    if not names:
        print("No matching JX1DX1 audio files were found on the page.", file=sys.stderr)
        return 1

    OUTPUT.mkdir(parents=True, exist_ok=True)
    downloaded = skipped = failed = 0
    for name in sorted(names):
        destination = OUTPUT / Path(name).name.replace(" ", "_")
        if destination.exists() and destination.stat().st_size:
            print(f"SKIP  {destination.name} (already exists)")
            skipped += 1
            continue

        try:
            result = get_json({
                "action": "query",
                "titles": "File:" + name,
                "prop": "imageinfo",
                "iiprop": "url",
                "format": "json",
            })
            pages = result.get("query", {}).get("pages", {})
            imageinfo = next(iter(pages.values())).get("imageinfo", [])
            if not imageinfo:
                raise RuntimeError("Fandom did not return a downloadable file URL")
            file_url = imageinfo[0]["url"]
            request = Request(file_url, headers={"User-Agent": "RansomdoorsAssetFetcher/1.0"})
            with urlopen(request, timeout=60) as response:
                data = response.read()
            if not data:
                raise RuntimeError("download was empty")
            destination.write_bytes(data)
            print(f"GET   {destination.name} ({len(data):,} bytes)")
            downloaded += 1
            time.sleep(0.25)
        except (HTTPError, URLError, KeyError, StopIteration, RuntimeError, TimeoutError) as exc:
            print(f"FAIL  {name}: {exc}", file=sys.stderr)
            failed += 1

    print(f"\nFinished: {downloaded} downloaded, {skipped} already present, {failed} failed.")
    print(f"Folder: {OUTPUT}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
