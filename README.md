# Star Citizen Hungarian Localization 4.10.1

Accent-free Hungarian localization for Star Citizen.

## Contents

- `Data/Localization/hungarian/global.ini` — Hungarian game text, with no accented Hungarian letters.
- `USER.cfg` — enables Hungarian text while retaining English audio.

## Install

Copy this repository's contents into the `LIVE` folder of a Star Citizen installation, preserving the directory structure:

```text
StarCitizen/LIVE/
├── Data/Localization/hungarian/global.ini
└── USER.cfg
```

`USER.cfg` contains:

```ini
g_language = hungarian
g_languageAudio = english
```

Back up an existing `USER.cfg` before replacing it. The localization file preserves the game entry order and runtime placeholders such as mission variables, formatting tags and newlines.
