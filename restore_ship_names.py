"""Restore original English ship display names in the Hungarian localization."""

from __future__ import annotations

from pathlib import Path
import re


CLEAN_ENGLISH = Path('E:/Star Citizen/StarCitizen/LIVE/data/Localization/english/global.ini.clean')
TARGETS = [
    Path('Data/Localization/hungarian/global.ini'),
    Path('E:/Star Citizen/StarCitizen/LIVE/data/Localization/hungarian/global.ini'),
]
SHIP_NAME_KEY = 'Event_ShipName_'
SHIP_DEALER_KEY = re.compile(r'^PU_SHIPDEALER\d+_M_CP_Pitch_ShipNameComment_')


def entries(path: Path) -> dict[str, str]:
    return {
        key: value
        for raw in path.read_text(encoding='utf-8-sig').splitlines()
        for key, separator, value in [raw.partition('=')]
        if separator
    }


def replace_insensitive(text: str, old: str, new: str) -> str:
    return re.sub(re.escape(old), new, text, flags=re.IGNORECASE)


def main() -> None:
    english = entries(CLEAN_ENGLISH)
    canonical = {key: value for key, value in english.items() if key.startswith(SHIP_NAME_KEY)}
    replacements_by_value: dict[str, str] = {}
    for key, original_name in canonical.items():
        # The current Hungarian name is read per target below. This mapping
        # remains key-based, avoiding an accidental replacement of ordinary
        # Hungarian words such as color or cargo labels.
        replacements_by_value[key] = original_name
    for target in TARGETS:
        raw = target.read_bytes()
        text = raw.decode('utf-8-sig')
        lines = text.splitlines(keepends=True)
        current = entries(target)
        translated_to_original = {
            current[key]: original
            for key, original in replacements_by_value.items()
            if key in current and current[key] != original and current[key]
        }
        changed_direct = changed_comments = 0
        rendered = []
        for source_line in lines:
            body = source_line.rstrip('\r\n')
            ending = source_line[len(body):]
            key, separator, value = body.partition('=')
            if key in canonical:
                value = canonical[key]
                changed_direct += 1
            elif SHIP_DEALER_KEY.match(key):
                previous = value
                # Only ship-dealer commentary is altered by value. This avoids
                # changing ordinary Hungarian words that resemble ship names.
                for translated, original in sorted(translated_to_original.items(), key=lambda pair: len(pair[0]), reverse=True):
                    value = replace_insensitive(value, translated, original)
                if value != previous:
                    changed_comments += 1
            rendered.append(f'{key}={value}{ending}')
        output = ''.join(rendered)
        if len(output.splitlines()) != len(lines):
            raise RuntimeError(f'Line count changed: {target}')
        target.write_bytes((b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'') + output.encode('utf-8'))
        print(f'{target}: restored {changed_direct} direct names; updated {changed_comments} dealer entries')


if __name__ == '__main__':
    main()
