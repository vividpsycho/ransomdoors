#!/usr/bin/env python3
"""Download all public audio files linked from the JX1DX1 Noli scrapped-skin page."""
from __future__ import annotations

import html
import json
import re
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, unquote, urlencode, urlparse
from urllib.request import Request, urlopen

BASE = "https://forsaken2024.fandom.com"
PAGE_URL = BASE + "/wiki/Noli/Skins/Scrapped"
API = BASE + "/api.php"
OUTPUT = Path("Assets/Sounds/Noli")
AUDIO_EXTENSIONS = {".mp3", ".ogg", ".oga", ".wav"}


def fetch(url: str) -> bytes:
    request = Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "text/html,application/json,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": BASE + "/",
    })
    with urlopen(request, timeout=45) as response:
        return response.read()


def api(params: dict[str, str]) -> dict:
    data = fetch(API + "?" + urlencode(params))
    return json.loads(data)


VOICE_FILES = [
    "JX1DX1Intro1.mp3",
    "JX1DX1IntroUnused.mp3",
    "JX1DX1Intro2.mp3",
    "JX1DX1Outro.mp3",
    "JX1DX1VoidRushStartup1.mp3",
    "JX1DX1VoidRushStartup2.mp3",
    "JX1DX1VoidRushStartup3.mp3",
    "JX1DX1VoidRushSlam1.mp3",
    "JX1DX1VoidRushSlam2.mp3",
    "JX1DX1VoidRushCrash.mp3",
    "JX1DX1Nova1.mp3",
    "JX1DX1Nova2.mp3",
    "JX1DX1Nova3.mp3",
    "JX1DX1ObservantStartup1.mp3",
    "JX1DX1ObservantStartup2.mp3",
    "JX1DX1ObservantTeleport1.mp3",
    "JX1DX1ObservantTeleport2.mp3",
    "JX1DX1Hallucination.mp3",
    "JX1DX1Stun1.mp3",
    "JX1DX1Stun2.mp3",
    "JX1DX1Stun3.mp3",
    "JX1DX1Stun4.mp3",
    "JX1DX1Kill1.mp3",
    "JX1DX1Kill2.mp3",
    "JX1DX1Kill3.mp3",
    "JX1DX1Kill4.mp3",
    "JX1DX1Kill5.mp3",
    "JX1DX1Kill6.mp3",
    "JX1DX1Kill007n7.mp3",
    "JX1DX1KillDeivy.mp3",
    "JX1DX1KillBuliderman.mp3",
    "JX1DX1KillDragondude3.mp3",
    "JX1DX1KillFOTL.mp3",
    "JX1DX1KillAubree1.mp3",
    "JX1DX1KillAubree2.mp3",
    "JX1DX1KillAubree3.mp3",
    "JX1DX1KillAubree4.mp3",
    "JX1DX1KillSpiders.mp3",
    "JX1DX1LMS1.mp3",
    "JX1DX1LMS2.mp3",
    "JX1DX1LMS3.mp3",
    "Jx1LMSthing.wav",
    "JX1DX1LMSDeivy.mp3",
    "JX1DX1LMSDragondude3.mp3",
    "JX1DX1LMSFOTL.mp3",
    "JX1DX1LMSAubree.mp3",
    "JX1DX1No1.mp3",
    "JX1DX1No2.mp3",
    "JX1DX1Yes1.mp3",
    "JX1DX1Yes2.mp3",
    "JX1DX1Taunt1.mp3",
    "JX1DX1Taunt2.mp3",
    "JX1DX1Rage1.mp3",
    "JX1DX1Rage2.mp3",
    "JX1DX1Laugh1.mp3",
    "JX1DX1Laugh2.mp3",
    "JX1DX1Laugh3.mp3",
    "JX1DX1IdleUnused1.mp3",
    "JX1DX1IdleUnused2.mp3",
    "JX1DX1LMSAubree2.ogg",
    "Jx1killdeivy.wav"
]


def discover_files() -> list[str]:
    # The wiki's public voiceline table provides these exact file names.
    # Avoid scraping its page HTML: Fandom blocks that endpoint for CI runners.
    return VOICE_FILES


def main() -> int:
    print("Reading audio links from the JX1DX1 scrapped-skin page")
    names = discover_files()
    if not names:
        print("No audio file links found in the public page HTML or API.", file=sys.stderr)
        return 1

    OUTPUT.mkdir(parents=True, exist_ok=True)
    downloaded = skipped = failed = 0
    for name in names:
        safe_name = name.replace("/", "_").replace(" ", "_")
        target = OUTPUT / safe_name
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
            if not info or not info[0].get("url"):
                raise RuntimeError("Fandom did not return a file URL")
            data = fetch(info[0]["url"])
            if not data:
                raise RuntimeError("empty response")
            target.write_bytes(data)
            downloaded += 1
            print(f"Downloaded {target.name} ({len(data):,} bytes)")
            time.sleep(0.15)
        except (HTTPError, URLError, KeyError, IndexError, RuntimeError, TimeoutError, ValueError) as exc:
            failed += 1
            print(f"FAILED {name}: {exc}", file=sys.stderr)

    print(f"\nResult: {downloaded} downloaded, {skipped} already present, {failed} failed.")
    print(f"Output: {OUTPUT}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
